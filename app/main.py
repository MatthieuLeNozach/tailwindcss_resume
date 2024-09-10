import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import subprocess
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
import yaml

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

# Load YAML content
with open("resume-content.yml", "r") as file:
    resume_data = yaml.safe_load(file)





@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager for FastAPI app. It will run all code before `yield`
    on app startup, and will run code after `yeld` on app shutdown. This method
    runs a subprocess on app startup which is the equivalent of running the
    tailwindcss command `tailwindcss -i ./src/tw.css -o ./css/main.css`.

    Must be passed as a property of the FastAPI app. (app = FastAPI(lifespan=lifespan))
    """

    if not os.path.exists('static/css'):
        os.makedirs('static/css')

    try:
        print(f"static/css/{resume_data['description']['tailwind_style']}.css")
        subprocess.run(
            [
                "tailwindcss",
                "-i",
                f"static/src/{resume_data['description']['tailwind_style']}.css",
                "-o",
                "static/css/main.css",
            ],
            check=True,
            #capture_output=True,
            #text=True
            
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"TailwindCSS generation failed: {e}")
    yield


app = FastAPI(lifespan=lifespan, default_response_class=HTMLResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Received request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status code: {response.status_code}")
    return response




templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request:Request):
    print(resume_data)
    return templates.TemplateResponse("base.html", {"request": request, "resume": resume_data})



from weasyprint import HTML
from fastapi.responses import FileResponse


@app.get("/export")
async def export_to_pdf(request: Request):
    # Render the HTML content without the footer
    html_content = templates.TemplateResponse("base.html", {"request": request, "resume": resume_data}).body.decode("utf-8")
    
    # Generate PDF from HTML using WeasyPrint
    pdf_file_path = 'resume.pdf'
    HTML(string=html_content).write_pdf(pdf_file_path)
    
    return FileResponse(pdf_file_path, media_type='application/pdf', filename='resume.pdf')