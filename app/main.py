import os
import argparse
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import subprocess
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
import yaml
import logging
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

def parse_args():
    parser = argparse.ArgumentParser(description="FastAPI Résumé App")
    parser.add_argument(
        "--yaml",
        default="resume-content.yml",
        help="Path to the YAML file containing resume content (default: ./resume-content.yml)"
    )
    return parser.parse_args()


def load_resume_data(filepath: str = "resume-content.yml"):
    with open(filepath, "r") as file:
        return yaml.safe_load(file)
    


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


global resume_data_file
args = parse_args()
resume_data_file = args.yaml
resume_data = load_resume_data(resume_data_file)

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
    
    global resume_data
    resume_data = load_resume_data(resume_data_file)
    #logger.info(resume_data)
    html_file = str(resume_data["description"]["html_file"])
    logger.info(f"HTML File: {html_file}")
    return templates.TemplateResponse(html_file, {"request": request, "resume": resume_data})


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0", 
        port=8000,       
        reload=True,
        reload_dirs=['.', 'static/css']
    )