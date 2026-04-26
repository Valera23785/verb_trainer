from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from storage.storage import load_verbs, load_progress, load_config
from core.scheduler import get_todays_verbs

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def dashboard(request: Request):
    verbs = load_verbs()
    progress = load_progress()
    config = load_config()
    todays_verbs = get_todays_verbs(verbs, progress, config)
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"todays_count": len(todays_verbs)})
