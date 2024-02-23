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
    prefix="/tasks",
    tags=['Tasks']
)

DISALLOWED_EXTENSIONS = ['.py', '.php', '.exe', '.sh']
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]
MAX_IMAGE_SIZE = 5 * 1024 * 1024
# Change in production environment to something outside of the backends root directory
IMAGEDIR = os.getcwd()

def contains_disallowed_extension(filename: str) -> bool:
    filename_lower = filename.lower()
    for ext in DISALLOWED_EXTENSIONS:
        print(ext)
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

def save_image_to_disk(contents: bytes, filename: str, task_name: str) -> str:
    image_dir = os.path.join(IMAGEDIR, f"images/{task_name}")
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    new_filename = generate_filename(filename, task_name)
    file_path = os.path.join(image_dir, new_filename)
    with open(file_path, "wb") as file:
        file.write(contents)
    return new_filename

# Get all tasks
@router.get("/", response_model=List[schemas.ReturnTask])
def get_tasks(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    query = db.query(models.Tasks).options(joinedload(models.Tasks.teams))
    if search:
        tasks = query.filter(models.Tasks.preferredSkillsets.contains(search)).limit(limit).offset(skip).all()
        return tasks
    else:
        tasks = query.all()
        return tasks

# Get completed tasks
@router.get("/completed", response_model=schemas.ReturnTask)
def get_completed(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    completedTask = db.query(models.Tasks).filter(models.Tasks.isCompleted == 'true').filter(models.Tasks.preferredSkillsets.contains(search)).limit(limit).offset(skip).all()
    return completedTask

# Get task photo
@router.get("/images/{id}")
async def get_task_image(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Tasks).filter(models.Tasks.id == id).first()
    if not task or not task.pictureName:  
        raise HTTPException(status_code=404, detail="Image not found")

    image_dir = os.path.join(IMAGEDIR, f"images/{task.name}")
    file_path = os.path.join(image_dir, task.pictureName)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find {task.pictureName}")
    return FileResponse(file_path)

# Get tasks by id
@router.get("/{id}", response_model=schemas.ReturnTask)
def get_task(id: int, db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    taskQuery = db.query(models.Tasks).where(models.Tasks.id == id).first()
    if taskQuery is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {id} not found.")
    else:
        task = db.query(models.Tasks).options(joinedload(models.Tasks.teams)).filter(models.Tasks.id == id).first()
    return task

# Create tasks
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ReturnCreatedTask)
def create_tasks(task: schemas.CreateTask, db: Session = Depends(get_db)):
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

# Upload task photo
@router.post("/images/{id}", status_code=status.HTTP_202_ACCEPTED)
async def upload_tasks_photo(id: int, photo: UploadFile = File(...), db: Session = Depends(get_db)):
    task = db.query(models.Tasks).filter(models.Tasks.id == id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task not found")
    contents = await photo.read()
    validate_upload_file(contents, photo)
    new_filename = save_image_to_disk(contents, photo.filename, task.name)
    task.pictureName = new_filename
    db.add(task)
    db.commit()
    return {"detail": f"Successfully uploaded {photo.filename} for {task.name}"}

# Update task by id 
@router.patch("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ReturnTask)
def update_task(id: int, update: schemas.UpdateTask = Body(...), db: Session = Depends(get_db)):
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
def delete_task(id: int, request_body: schemas.DeleteTask = Body(...), db: Session = Depends(get_db)):
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
def join_task(id: int, join: schemas.JoinTask, db: Session = Depends(get_db)):
    task = db.query(models.Tasks).filter(models.Tasks.id == id).first()
    team = db.query(models.Teams).filter(models.Teams.name == join.team_name).first()
    captainCode = team.captainCode
    print(captainCode)
    print(join.captainCode)
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team was not found.")
    if team.task_id != None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Team is already assigned to a task, please delete previous task before selecting a new one.")
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task id: {id} does not exist.")
    if captainCode != join.captainCode:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You entered the wrong Captain Code.")
    
    team.task_id = id
    db.commit()
    db.refresh(team)
    return task