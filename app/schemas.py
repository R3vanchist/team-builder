from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Members
class CreateMember(BaseModel):
    name: str
    skillsets: str

class GetMember(BaseModel):
    skillsets: str
    teamName: Optional[str]

class ReturnMember(BaseModel):
    id: int
    name: str
    skillsets: str
    class Config:
        orm_mode = True

class UpdateMember(BaseModel):
    name: Optional[str]
    skillsets: Optional[str]

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
    description: Optional[str]
    classification: Optional[str]
    preferredSkillsets: Optional[str]
    desiredDeliverable: Optional[str]
    organization: Optional[str]
    location: Optional[str]
    pocName: Optional[str]
    pocDiscordName: Optional[str]
    dataSupplied: Optional[bool]

# Teams
class CreateTeam(BaseModel):
    captainDiscordName: str
    gitRepo: str
    task: Optional[str]
    location: str
    preferredWorkTime: str
    classification: str
    preferredSkillsets: str
    member: ReturnMember

class GetTeam(BaseModel):
    captainDiscordName: str
    gitRepo: str
    task: Optional[str]
    location: str
    preferredWorkTime: str
    classification: str
    preferredSkillsets: str
    member: ReturnMember

class ReturnTeam(BaseModel):
    captainDiscordName: str
    gitRepo: str
    task: Optional[str]
    location: str
    preferredWorkTime: str
    classification: str
    preferredSkillsets: str
    captainCode: str
    member: ReturnMember
    class Config:
        orm_mode = True

class UpdateTeam(BaseModel):
    captainCode: str
    captainDiscordName: Optional[str]
    gitRepo: Optional[str]
    task: Optional[str]
    location: Optional[str]
    preferredWorkTime: Optional[str]
    classification: Optional[str]
    preferredSkillsets: Optional[str]
    member: Optional[ReturnMember]