import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sentry_sdk

load_dotenv()

# Initialize Sentry
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")
templates.env.globals["POSTHOG_API_KEY"] = os.getenv("POSTHOG_API_KEY")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html",
        context={"title": "Pin Hill Conservation Land"}
    )

@app.get("/history", response_class=HTMLResponse)
async def read_history(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="history.html",
        context={"title": "History - Pin Hill Conservation Land"}
    )

@app.get("/trails", response_class=HTMLResponse)
async def read_trails(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="trails.html",
        context={"title": "Trails - Pin Hill Conservation Land"}
    )
