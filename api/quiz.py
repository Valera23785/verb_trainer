from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from storage.storage import load_progress, load_verbs, load_config, save_progress
from core.scheduler import get_todays_verbs
from core.quiz import update_progress



router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/quiz")
def read_quiz(request: Request):
    verbs = load_verbs()
    progress = load_progress()
    config = load_config()
    verbs_today = get_todays_verbs(verbs, progress, config)
    verb = verbs_today[0] if verbs_today else None 
    return templates.TemplateResponse(request=request, name="quiz.html", context={"verb": verb})

@router.post("/quiz/check")
def check_answer(answer: str = Form(...), verb_id: int = Form(...)):
    verbs = load_verbs()
    verb = next((v for v in verbs if v.id == verb_id), None)
    if verb is None:
        return RedirectResponse(url=f"/quiz", status_code=303)
    correct = answer.strip().lower() == verb.russian.lower()
    progress = load_progress()
    config = load_config()
    update_progress(verb, progress, correct, config)
    save_progress(progress)
    return RedirectResponse(url=f"/quiz/result?correct={correct}&verb_id={verb_id}", status_code=303)

@router.get("/quiz/result")
def quiz_result(request: Request, correct: bool, verb_id: int):
    verbs = load_verbs()
    verb = next((v for v in verbs if v.id == verb_id), None)
    return templates.TemplateResponse(request=request, name="quiz_result.html", context={"correct": correct, "verb": verb})
