from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

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
