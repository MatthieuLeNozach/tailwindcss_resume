import { Config } from "tailwindcss";

const config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./templates/**/*.html",
    "./static/src/**/*.css",
  ],
  theme: {
    extend: {
      screens: {
        sm: '480px',
        md: '768px',
        lg: '976px',
        xl: '1440px',
        a4: { raw: "(min-width: 794px) and (min-height: 1123px)" },
      },
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        'tahiti': {
          100: '#cffafe',
          200: '#a5f3fc',
          300: '#67e8f9',
          400: '#22d3ee',
          500: '#06b6d4',
          600: '#0891b2',
          700: '#0e7490',
          800: '#155e75',
          900: '#164e63',
        },
        'bismarck': {
          100: '#73c5e0',
          200: '#68b1ca',
          300: '#5c9eb3',
          400: '#518a9d',
          500: '#457686',
          600: '#3a6370',
          700: '#2e4f5a',
          800: '#223b43',
          900: '#17272d',
          950: '#0b1416'
        },
      },
      fontFamily: {
        sans: ['Poppins', 'sans-serif'],
        serif: ['Lora', 'serif'],
      },
      fontWeight: {
        light: 100,
        normal: 400,
        medium: 500,
        bold: 700,
      },
      fontSize: {
        xs: '0.75rem', // 12px
        sm: '0.875rem', // 14px
        base: '1rem', // 16px
        lg: '1.125rem', // 18px
        xl: '1.25rem', // 20px
        '2xl': '1.5rem', // 24px
        '3xl': '1.875rem', // 30px
        '4xl': '2.25rem', // 36px
        '5xl': '3rem', // 48px
        '6xl': '3.75rem', // 60px
      },
      spacing: {
        '1': '8px',
        '2': '12px',
        '3': '16px',
        '4': '24px',
        '5': '32px',
        '6': '48px',
        '8xl': '96rem',
        '9xl': '128rem',
      },
      borderRadius: {
        '4xl': '2rem',
      },
      backgroundImage: {
        'title-bar-gradient': 'linear-gradient(to right, #17272d, rgba(11, 20, 22, 0))',      },
    },
  },
  plugins: [],
  corePlugins: {
    fontIcons: true,
  },
};

export default config;
