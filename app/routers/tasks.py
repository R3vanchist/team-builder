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
    prefix="/tasks",
    tags=['Tasks']
)

# Get all tasks
@router.get("/", response_model=List[schemas.ReturnTask])
def getTasks(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    query = db.query(models.Tasks).options(joinedload(models.Tasks.teams))
    if search:
        tasks = query.filter(models.Tasks.preferredSkillsets.contains(search)).limit(limit).offset(skip).all()
        return tasks
    else:
        tasks = query.all()
        return tasks

# Get completed tasks
# update the response model
@router.get("/completed", response_model=schemas.ReturnTask)
def getCompleted(db: Session = Depends(get_db)):
    completedTask = db.query(models.Tasks).filter(models.Tasks.isCompleted == 'true').all()
    return completedTask

# Get tasks by id
@router.get("/{id}", response_model=schemas.ReturnTask)
def getTasks(id: int, db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    taskQuery = db.query(models.Tasks).where(models.Tasks.id == id).first()
    if taskQuery is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {id} not found.")
    else:
        task = db.query(models.Tasks).options(joinedload(models.Tasks.teams)).filter(models.Tasks.id == id).first()
    return task

# Create tasks
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ReturnCreatedTask)
def createTasks(task: schemas.CreateTask, db: Session = Depends(get_db)):
    # Function to generate a taskCode
    def taskCodeGenerator(length=6):
        chars = string.ascii_letters
        taskCode = ''.join(random.choice(chars) for _ in range(length))
        return taskCode
    taskCode = taskCodeGenerator(length=6)

    # Create a new task entry
    newTaskData = task.dict()
    newTask = models.Tasks(**newTaskData, taskCode=taskCode)
    db.add(newTask)
    db.commit()
    db.refresh(newTask)
    return newTask

# Update task by id 
# update the schema for response model, need to pull isCompleted
@router.patch("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ReturnTask)
def updateTask(id: int, update: schemas.UpdateTask = Body(...), db: Session = Depends(get_db)):
    taskName= db.query(models.Tasks.name).filter(models.Tasks.id == id).first()
    taskCode = db.query(models.Tasks.taskCode).filter(models.Tasks.id == id).first()
    taskQuery = db.query(models.Tasks).filter(models.Tasks.id == id)
    taskUpdate = update.dict(exclude_unset=True, exclude_none=True)
    task = taskQuery.first()

    if task == None:
        raise HTTPException(status_code=404, detail=f"{taskName} not found")
    
    if taskCode[0] != update.taskCode:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Task code was invalid.")
    else:
        taskQuery.update(taskUpdate)
        db.commit()
        
        return task

# Delete a task
@router.put("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteTask(id: int, request_body: schemas.DeleteTask = Body(...), db: Session = Depends(get_db)):
    taskQuery = db.query(models.Tasks).filter(models.Tasks.id == id)
    task = taskQuery.first()

    taskCodeQuery = db.query(models.Tasks.taskCode).filter(models.Tasks.id == id)
    taskCodeResult = taskCodeQuery.first()
    taskCode = taskCodeResult[0]

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {id} does not exist.")

    if taskCode != request_body.taskCode:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid task code.")

    taskQuery.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Join a task
@router.post("/{id}/join", status_code=status.HTTP_201_CREATED, response_model=schemas.ReturnTask)
def joinTask(id: int, join: schemas.JoinTask, db: Session = Depends(get_db)):
    task = db.query(models.Tasks).filter(models.Tasks.id == id).first()
    team = db.query(models.Teams).filter(models.Teams.id == join.team_id).first()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team was not found.")
    if team.task_id != None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Team is already assigned to a task, please delete previous task before selecting a new one.")
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task id: {id} does not exist.")
    else:
        team.task_id = id
        db.commit()
        db.refresh(team)
        return task