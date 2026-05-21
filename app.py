from fastapi import FastAPI
from api.dashboard import router as dashboard_router


app = FastAPI()

app.include_router(dashboard_router)

@app.get("/")
def read_root():
    return {"status": "ok"}

