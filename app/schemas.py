from pydantic import BaseModel, root_validator, Field
from datetime import datetime
from typing import Optional, List

# Tasks
class CreateTask(BaseModel):
    name: str
    description: str
    classificationLevel: str
    preferredSkillsets: str
    desiredDeliverable: str
    organization: str
    location: str
    pocName: str
    pocDiscordName: str
    hasData: Optional[bool] = False
    class Config:
        orm_mode = True

class DeleteTask(BaseModel):
    taskCode: str

class UpdateTask(BaseModel):
    taskCode: str
    name: Optional[str] = None
    description: Optional[str] = None
    classificationLevel: Optional[str] = None
    preferredSkillsets: Optional[str] = None
    desiredDeliverable: Optional[str] = None
    organization: Optional[str] = None
    location: Optional[str] = None
    pocName: Optional[str] = None
    pocDiscordName: Optional[str] = None
    hasData: Optional[bool] = None
    isCompleted: Optional[bool] = None

class JoinTask(BaseModel):
    team_id: int

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
    team_id: int
    class Config:
        orm_mode = True

class CreateTeamCaptain(CreateMember):
    pass

class ReturnCaptain(ReturnMember):
    pass

# Teams
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
    needsMembers: bool
    members: List[ReturnMember] = []
    class Config:
        orm_mode = True

class DeleteTeam(BaseModel):
    captainCode: str
    team_id: int

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
    
class ReturnCreatedTeam(ReturnTeam):
    captainCode: str
    pass

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
    needsMembers: Optional[bool] = None

class ReturnTask(BaseModel):
    id: int
    name: str
    description: str
    classificationLevel: str
    preferredSkillsets: str
    desiredDeliverable: str
    organization: str
    location: str
    pocName: str
    pocDiscordName: str
    hasData: bool
    isCompleted: bool
    teams: List[ReturnTeam] = []
    class Config:
        orm_mode = True

class ReturnCreatedTask(ReturnTask):
    taskCode: str
    pass
