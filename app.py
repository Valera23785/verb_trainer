from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root():
    return {"status": "ok"}


@app.get("/dashboard")
def read_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html", context={"verb_count": 5, "streak": 3})

