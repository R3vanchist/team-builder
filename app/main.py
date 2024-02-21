from fastapi import FastAPI
from .routers import members, tasks, teams
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=["*"],
)

app.include_router(tasks.router)
app.include_router(teams.router)
app.include_router(members.router)

@app.get("/")
def read():
    return {"Message": "Welcome to the Team Builder API"}
