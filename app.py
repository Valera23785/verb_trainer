from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from storage.storage import load_progress, load_verbs, load_config
from core.scheduler import get_todays_verbs
from core.stats import get_learned_count, get_streak


app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root():
    return {"status": "ok"}


@app.get("/dashboard")
def read_dashboard(request: Request):
    verbs = load_verbs()
    progress = load_progress()
    config = load_config()
    verb_count = len(get_todays_verbs(verbs, progress, config))
    learned_count = get_learned_count(progress)
    streak = get_streak(progress)
    return templates.TemplateResponse(request=request, name="dashboard.html", context={"verb_count": verb_count, "streak": streak, "learned_count": learned_count})

