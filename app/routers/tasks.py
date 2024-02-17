from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.sql.functions import func
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/tasks",
    tags=['Tasks']
)

# Get all tasks
@router.get("/", response_model=List[schemas.GetTask])
def read_root():
    return {"Hello": "World"}

# Create taks
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CreateTask)
def read_root():
    return {"Hello": "World"}

# Get tasks by id
@router.get("/{id}", response_model=schemas.ReturnTask)
def read_root():
    return {"Hello": "World"}

# Update task by id 
@router.put("/", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UpdateTask)
def read_root():
    return {"Hello": "World"}

# Delete a task
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def read_root():
    return {"Hello": "World"}