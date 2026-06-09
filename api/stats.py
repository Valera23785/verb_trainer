from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/stats")
def read_stats(request: Request):
    return templates.TemplateResponse(request=request, name="stats.html", context={"content": "Coming soon"})



