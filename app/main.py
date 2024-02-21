from fastapi import FastAPI
from .routers import members, tasks, teams

app = FastAPI()

app.include_router(tasks.router)
app.include_router(teams.router)
app.include_router(members.router)

@app.get("/")
def read():
    return {"Hello": "World"}
