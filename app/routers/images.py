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
from random import randint
import os


router = APIRouter(
    prefix="/images",
    tags=['Upload']
)

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]
MAX_IMAGE_SIZE = 5 * 1024 * 1024
IMAGEDIR = os.getcwd()


# Upload team photo
@router.post("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def upload_teams(id: int, photo: UploadFile = File(...), db: Session = Depends(get_db)):
    team = db.query(models.Teams).filter(models.Teams.id == id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found.")
    
    contents = await photo.read()
    if contents is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No file uploaded.")
    if len(contents) > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=f"{photo.filename} is too large.")
    if photo.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{photo.filename} file type is not valid.")
    if ".." in photo.filename or photo.filename.startswith("/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image name.")
    
    image_dir = os.path.join(IMAGEDIR, "images")
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    
    file_path = os.path.join(image_dir, photo.filename)
    with open(file_path, "wb") as file:
        file.write(contents)
    
    return {"detail": f"Successfully uploaded {photo.filename} for team {team.name}."}

# Get teams photo
@router.get("/{id}")
async def getTeamPicture(id: int):
    print(image_dir)
    return "Hello World:)"