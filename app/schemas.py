from pydantic import BaseModel, root_validator
from datetime import datetime
from typing import Optional

# Tasks
class CreateTask(BaseModel):
    description: str
    classificationLevel: str
    preferredSkillsets: str
    desiredDeliverable: str
    organization: str
    location: str
    pocName: str
    pocDiscordName: str
    dataSupplied: bool = False

class GetTask(BaseModel):
    description: str
    classificationLevel: str
    preferredSkillsets: str
    desiredDeliverable: str
    organization: str
    location: str
    pocName: str
    pocDiscordName: str
    dataSupplied: bool = False

class ReturnTask(BaseModel):
    description: str
    classificationLevel: str
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
    classificationLevel: Optional[str] = None
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

class ReturnMember(BaseModel):
    id: int
    name: str
    discordName: str
    skillsets: str
    teamId: int

    class Config:
        orm_mode = True

class Delete(BaseModel):
    captainCode: str
    teamId: int

# Teams
class CreateTeamCaptain(CreateMember):
    pass
class CreateTeam(BaseModel):
    name: str
    captainDiscordName: Optional[str] = None 
    gitRepo: str
    task: Optional[str] = None
    location: str
    preferredWorkTime: str
    classificationLevel: str
    preferredSkillsets: str
    captain: CreateTeamCaptain

    @root_validator(pre=True)
    def populate_captain_discord_name(cls, values):
        captain = values.get('captain')
        if captain:
            # Access the discordName using dictionary key access
            values['captainDiscordName'] = captain.get('discordName', '')
        return values
    

class ReturnCaptain(ReturnMember):
    pass

class ReturnTeam(BaseModel):
    id: int
    name: str
    captainDiscordName: str
    gitRepo: str
    task: Optional[str] = None
    location: str
    preferredWorkTime: str
    classificationLevel: str
    preferredSkillsets: str
    # captainCode showing back up to the user is an issue
    captainCode: Optional[str] = None
    member: ReturnCaptain
    class Config:
        orm_mode = True

class GetTeams(BaseModel):
    id: int
    name: str
    captainDiscordName: str
    gitRepo: str
    task: Optional[str] = None
    location: str
    preferredWorkTime: str
    classificationLevel: str
    preferredSkillsets: str
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
    classificationLevel: Optional[str] = None
    preferredSkillsets: Optional[str] = None
    member: Optional[ReturnMember] = None

class GetMember(BaseModel):
    id: int
    name: str
    discordName: str
    skillsets: str
    teamName: Optional[ReturnTeam] = None