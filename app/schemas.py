from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Tasks
class CreateTask(BaseModel):
    description: str
    classification: str
    preferredSkillsets: str
    desiredDeliverable: str
    organization: str
    location: str
    pocName: str
    pocDiscordName: str
    dataSupplied: bool = False

class GetTask(BaseModel):
    description: str
    classification: str
    preferredSkillsets: str
    desiredDeliverable: str
    organization: str
    location: str
    pocName: str
    pocDiscordName: str
    dataSupplied: bool = False

class ReturnTask(BaseModel):
    description: str
    classification: str
    preferredSkillsets: str
    desiredDeliverable: str
    organization: str
    location: str
    pocName: str
    pocDiscordName: str
    taskCode: str
    dataSupplied: bool
    class Config:
        orm_mode = True

class UpdateTask(BaseModel):
    taskCode: str
    description: Optional[str] = None
    classification: Optional[str] = None
    preferredSkillsets: Optional[str] = None
    desiredDeliverable: Optional[str] = None
    organization: Optional[str] = None
    location: Optional[str] = None
    pocName: Optional[str] = None
    pocDiscordName: Optional[str] = None
    dataSupplied: Optional[bool] = None

# Members
class CreateMember(BaseModel):
    name: str
    discordName: str
    skillsets: str
    teamId: Optional[int] = None

class ReturnMember(BaseModel):
    id: int
    name: str
    discordName: str
    skillsets: str
    class Config:
        orm_mode = True

class UpdateMember(BaseModel):
    name: Optional[str] = None
    skillsets: Optional[str] = None

class DeleteRequestBody(BaseModel):
    captainCode: str
    teamId: int

# Teams
class CreateTeam(BaseModel):
    name: str
    captainDiscordName: str
    gitRepo: str
    task: Optional[str] = None
    location: str
    preferredWorkTime: str
    classification: str
    preferredSkillsets: str

class GetTeam(BaseModel):
    name: str
    captainDiscordName: str
    gitRepo: str
    task: Optional[str] = None
    location: str
    preferredWorkTime: str
    classification: str
    preferredSkillsets: str
    member: ReturnMember

class ReturnTeam(BaseModel):
    name: str
    captainDiscordName: str
    gitRepo: str
    task: Optional[str] = None
    location: str
    preferredWorkTime: str
    classification: str
    preferredSkillsets: str
    captainCode: str
    member: ReturnMember
    class Config:
        orm_mode = True

class UpdateTeam(BaseModel):
    name: Optional[str] = None
    captainCode: str
    captainDiscordName: Optional[str] = None
    gitRepo: Optional[str] = None
    task: Optional[str] = None
    location: Optional[str] = None
    preferredWorkTime: Optional[str] = None
    classification: Optional[str] = None
    preferredSkillsets: Optional[str] = None
    member: Optional[ReturnMember] = None

class GetMember(BaseModel):
    id: int
    name: str
    discordName: str
    skillsets: str
    teamName: Optional[ReturnTeam] = None