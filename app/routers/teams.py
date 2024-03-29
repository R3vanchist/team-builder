from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Body, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional, Tuple
import random
import string
import os
from .. import models, schemas
from ..database import get_db
from ..security import generate_filename


router = APIRouter(
    prefix="/teams",
    tags=['Teams']
)
DISALLOWED_EXTENSIONS = ['.py', '.php', '.exe', '.sh']
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]
MAX_IMAGE_SIZE = 5 * 1024 * 1024
# Change in production environment to something outside of the backends root directory
IMAGEDIR = os.getcwd()

def contains_disallowed_extension(filename: str) -> bool:
    filename_lower = filename.lower()
    for ext in DISALLOWED_EXTENSIONS:
        if ext in filename_lower:
            return True
    return False
    
def validate_upload_file(contents: bytes, photo: UploadFile) -> Tuple[bytes, str]:
    if contents is None or len(contents) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No file uploaded.")
    if contains_disallowed_extension(photo.filename) == True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"No, No, No!")
    if len(contents) > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=f"{photo.filename} is too large.")
    if photo.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{photo.filename} file type is not valid.")
    if ".." in photo.filename or photo.filename.startswith("/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image name.")

    return contents, photo.filename

def save_image_to_disk(contents: bytes, filename: str, team_name: str) -> str:
    image_dir = os.path.join(IMAGEDIR, f"images/{team_name}")
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    new_filename = generate_filename(filename, team_name)
    file_path = os.path.join(image_dir, new_filename)
    with open(file_path, "wb") as file:
        file.write(contents)
    return new_filename

# Get all teams
@router.get("/", response_model=List[schemas.ReturnTeam])
def get_teams(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    query = db.query(models.Teams).options(joinedload(models.Teams.members))
    if search:
        teams = query.filter(models.Teams.preferredSkillsets.contains(search)).limit(limit).offset(skip).all()
        return teams
    else:
        teams = query.all()
        return teams

# Get teams photo
@router.get("/images/{id}")
async def get_team_image(id: int, db: Session = Depends(get_db)):
    team = db.query(models.Teams).filter(models.Teams.id == id).first()
    if not team or not team.pictureName:  
        raise HTTPException(status_code=404, detail="Image not found")

    image_dir = os.path.join(IMAGEDIR, f"images/{team.name}")
    file_path = os.path.join(image_dir, team.pictureName)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find {team.pictureName}")
    return FileResponse(file_path)

# Get team by id
@router.get("/{id}", response_model=schemas.ReturnTeam)
def get_team(id: int, db: Session = Depends(get_db)):
    team = db.query(models.Teams).options(joinedload(models.Teams.members)).filter(models.Teams.id == id).first()
    return team

# Create teams
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ReturnCreatedTeam)
def create_team(team: schemas.CreateTeam, db: Session = Depends(get_db)):
    # Function to generate a captainCode
    def captainCodeGenerator(length=6):
        chars = string.ascii_letters
        captainCode = ''.join(random.choice(chars) for _ in range(length))
        return captainCode
    captainCode = captainCodeGenerator(length=6)
    existingTeams = db.query(models.Teams.name).all()


    # Create a new team entry
    newTeamData = team.dict(exclude={"captain"})
    newTeam = models.Teams(**newTeamData, captainCode=captainCode)
    
    # Check to see if team already exists
    for i in existingTeams:
        if team.name == i[0]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Sorry, a team with name {team.name} already exists.")
    
    db.add(newTeam)
    db.commit()
    db.refresh(newTeam)

    captainData = team.captain.dict()
    newMember = models.Members(**captainData, team_id=newTeam.id)
    db.add(newMember)
    db.commit()
    db.refresh(newMember)
    return newTeam 

# Update team by id 
@router.patch("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ReturnTeam)
def update_team(id: int, update: schemas.UpdateTeam, db: Session = Depends(get_db)):
    teamName= db.query(models.Teams.name).filter(models.Teams.id == id).first()
    captainCode = db.query(models.Teams.captainCode).filter(models.Teams.id == id).first()
    teamQuery = db.query(models.Teams).filter(models.Teams.id == id)
    teamUpdate = update.dict(exclude_unset=True, exclude_none=True)
    team = teamQuery.first()

    if team == None:
        raise HTTPException(status_code=404, detail=f"{teamName} not found")
    
    if captainCode[0] != update.captainCode:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Captain code was invalid.")
    else:
        teamQuery.update(teamUpdate)
        db.commit()
        
        return team

# Delete a team
@router.put("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(id: int, request_body: schemas.DeleteTeam = Body(...), db: Session = Depends(get_db)):
    teamQuery = db.query(models.Teams).filter(models.Teams.id == id)
    team = teamQuery.first()

    captainCodeQuery = db.query(models.Teams.captainCode).filter(models.Teams.id == id)
    captainCodeResult = captainCodeQuery.first()
    captainCode = captainCodeResult[0]

    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team with id: {id} does not exist.")

    if captainCode != request_body.captainCode:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid captain code.")

    teamQuery.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Upload team photo
@router.post("/images/{id}", status_code=status.HTTP_202_ACCEPTED)
async def upload_teams_photo(id: int, photo: UploadFile = File(...), db: Session = Depends(get_db)):
    team = db.query(models.Teams).filter(models.Teams.id == id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team not found")
    contents = await photo.read()
    validate_upload_file(contents, photo)
    new_filename = save_image_to_disk(contents, photo.filename, team.name)
    team.pictureName = new_filename
    db.add(team)
    db.commit()
    return {"detail": f"Successfully uploaded {photo.filename} for {team.name}"}

# Create members
@router.post("/{id}/join", status_code=status.HTTP_201_CREATED, response_model=schemas.CreateMember)
def create_member(id: int, member: schemas.CreateMember, db: Session = Depends(get_db)):
    newMember = models.Members(**member.dict(), team_id=id)
    db.add(newMember)
    db.commit()
    db.refresh(newMember)
    return newMember
