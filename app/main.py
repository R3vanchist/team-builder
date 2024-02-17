from fastapi import FastAPI
from . import models
from .database import engine
from .routers import members, tasks, teams
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tasks.router)
app.include_router(teams.router)
app.include_router(members.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
