from fastapi import FastAPI
from .routers import members, tasks, teams, upload
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

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
app.include_router(upload.router)

@app.get("/")
def read():
    return {"Message": "Welcome to the Team Builder API"}

#if __name__ == "__main__":
#    uvicorn.run(app, host="127.0.0.1", port=8000)