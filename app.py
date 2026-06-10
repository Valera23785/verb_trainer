from fastapi import FastAPI
from api.dashboard import router as dashboard_router
from api.quiz import router as quiz_router
from api.stats import router as stats_router
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.include_router(dashboard_router)
app.include_router(quiz_router)
app.include_router(stats_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"status": "ok"}

