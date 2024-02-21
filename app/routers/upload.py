from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Body, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
import random
import string
from sqlalchemy import func, select, text
from sqlalchemy.sql.functions import func
from .. import models, schemas
from ..database import get_db
import uuid 
import os
from random import randint

router = APIRouter(
    prefix="/images",
    tags=['Images Uploaded']
)

IMAGEDIR = "../images/"

@router.post("/teams")
async def uploadTeams(photo: UploadFile = File(...), db: Session = Depends(get_db)):
    photo.filename = f"{uuid.uuid4()}.jpg"
    contents = await photo.read()
    with open(f"{IMAGEDIR}{photo.filename}", "wb") as f:
        f.write(contents)
    return {"Image succesfully uploaded": photo.filename}

@router.get("/show/")
async def showTeams():
    files = os.listdir(IMAGEDIR)
    random_index = randint(0, len(files) -1)
    path = f"{IMAGEDIR}{files[random_index]}"
    return FileResponse(path)