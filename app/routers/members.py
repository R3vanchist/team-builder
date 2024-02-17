from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/members",
    tags=['Members']
)

# Get all members
@router.get("/", response_model=List[schemas.GetMember])

# Create members
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CreateMember)

# Get members by id
@router.get("/{id}", response_model=schemas.ReturnMember)

# Update member by id 
@router.put("/", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UpdateMember)

# Delete a member
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)