from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.sql.functions import func
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/teams",
    tags=['Teams']
)

# Get all teams
@router.get("/", response_model=List[schemas.GetTeam])
def read_root():
    return {"Hello": "World"}

# Create teams
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CreateTeam)
def read_root():
    return {"Hello": "World"}

# Get team by id
@router.get("/{id}", response_model=schemas.GetTeam)
def read_root():
    return {"Hello": "World"}

# Update team by id 
@router.put("/", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UpdateTeam)
def read_root():
    return {"Hello": "World"}

# Delete a team
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def read_root():
    return {"Hello": "World"}