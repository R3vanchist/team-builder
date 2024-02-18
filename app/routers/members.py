from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, Body
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.sql.functions import func
from  .. import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/members",
    tags=['Members']
)

# Get all members
@router.get("/", response_model=List[schemas.ReturnMember])
def getMembers(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    members = db.query(models.Members).filter(models.Members.name.contains(search)).limit(limit).offset(skip).all()

    return members

# Get members by id
@router.get("/{id}", response_model=schemas.ReturnMember)
def getMember(id: int, db: Session = Depends(get_db)):
    member = db.query(models.Members).filter(models.Members.id == id).first()
    teamNameQuery = db.query(models.Teams.name).join(models.Members, models.Members.team_id == models.Teams.id, isouter=True).first()
    teamName = teamNameQuery[0]
    teamNamejson = {
        "teamName": teamName
    }
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist.")
    return member, teamNamejson


# Delete a member
@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteMember(id: int, request_body: schemas.DeleteTeam = Body(...), db: Session = Depends(get_db)):
    memberQuery = db.query(models.Members).filter(models.Members.id == id)
    member = memberQuery.first()

    captainCodeQuery = db.query(models.Teams.captainCode).filter(models.Teams.id == id)
    captainCodeResult = captainCodeQuery.first()
    captainCode = captainCodeResult[0]

    if member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Member with id: {id} does not exist.")

    if captainCode != request_body.captainCode:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid captain code.")

    memberQuery.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)