from pydantic import BaseModel, root_validator, Field
from datetime import datetime
from typing import Optional, List

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
    
    class Config:
        orm_mode = True

class ReturnMember(BaseModel):
    id: int
    name: str
    discordName: str
    skillsets: str
    team_id: int
    teamName: Optional[str] = None

    class Config:
        orm_mode = True

class Delete(BaseModel):
    captainCode: str
    team_id: int

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

class ReturnCreatedTeam(ReturnTeam):
    captainCode: str
    pass

class UpdateTeam(BaseModel):
    name: Optional[str] = Field(default=...)
    captainCode: str
    captainDiscordName: Optional[str] = Field(default=...)
    gitRepo: Optional[str] = Field(default=...)
    task: Optional[str] = Field(default=...)
    location: Optional[str] = Field(default=...)
    preferredWorkTime: Optional[str] = Field(default=...)
    classificationLevel: Optional[str] = Field(default=...)
    preferredSkillsets: Optional[str] = Field(default=...)
    needsMembers: Optional[bool] = Field(default=...)

class TeamsResponse(BaseModel):
    team: ReturnTeam
    member: ReturnMember