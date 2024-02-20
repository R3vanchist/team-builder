from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Body
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
import random
import string
from sqlalchemy import func, select, text
from sqlalchemy.sql.functions import func
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/teams",
    tags=['Teams']
)

# Get all teams
@router.get("/", response_model=List[schemas.ReturnTeam])
def getTeams(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    query = db.query(models.Teams).options(joinedload(models.Teams.members))
    if search:
        teams = query.filter(models.Teams.preferredSkillsets.contains(search)).limit(limit).offset(skip).all()
        return teams
    else:
        teams = query.all()
        return teams


# Get team by id
@router.get("/{id}", response_model=schemas.ReturnTeam)
def getTeam(id: int, db: Session = Depends(get_db)):
    team = db.query(models.Teams).options(joinedload(models.Teams.members)).filter(models.Teams.id == id).first()
    return team

# Create teams
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ReturnCreatedTeam)
def createTeam(team: schemas.CreateTeam, db: Session = Depends(get_db)):
    # Function to generate a captainCode
    def captainCodeGenerator(length=6):
        chars = string.ascii_letters
        captainCode = ''.join(random.choice(chars) for _ in range(length))
        return captainCode
    captainCode = captainCodeGenerator(length=6)

    # Create a new team entry
    newTeamData = team.dict(exclude={"captain"})
    newTeam = models.Teams(**newTeamData, captainCode=captainCode)
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
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ReturnTeam)
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
def deleteMember(id: int, request_body: schemas.DeleteTeam = Body(...), db: Session = Depends(get_db)):
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

# Create members
@router.post("/{id}/join", status_code=status.HTTP_201_CREATED, response_model=schemas.CreateMember)
def createMember(id: int, member: schemas.CreateMember, db: Session = Depends(get_db)):
    newMember = models.Members(**member.dict(), team_id=id)
    db.add(newMember)
    db.commit()
    db.refresh(newMember)
    return newMember
