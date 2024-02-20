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
    task_id: int

class ReturnTask(BaseModel):
    id: int
    description: str
    classificationLevel: str
    preferredSkillsets: str
    desiredDeliverable: str
    organization: str
    location: str
    pocName: str
    pocDiscordName: str
    hasData: bool
    team_id: Optional[int] = None
    class Config:
        orm_mode = True

class ReturnCreatedTask(ReturnTask):
    taskCode: str
    pass

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
    teamName: Optional[str] = None
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
    Team: ReturnTeam
    Member: ReturnMember

class ReturnTaskAndTeams(BaseModel):
    tasks: ReturnTask
    teams: ReturnTeam