from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    team_id = Column(Integer, nullable=True)
    description = Column(String, nullable=False)
    classificationLevel = Column(String, nullable=False)
    preferredSkillsets = Column(String, nullable=False)
    desiredDeliverable = Column(String, nullable=False)
    organization = Column(String, nullable=False)
    location = Column(String, nullable=False)
    pocName = Column(String, nullable=False)
    pocDiscordName = Column(String, nullable=False)
    hasData = Column(Boolean, server_default='FALSE', nullable=False)
    taskCode = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    isCompleted = Column(Boolean, server_default='FALSE', nullable=False)
    teams = relationship("Teams", back_populates="tasks")


class Teams(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    captainDiscordName = Column(String, nullable=False)
    gitRepo = Column(String, nullable=True)
    location = Column(String, nullable=False)
    preferredWorkTime = Column(String, nullable=False)
    classificationLevel = Column(String, nullable=False)
    preferredSkillsets = Column(String, nullable=False)
    needsMembers = Column(Boolean, nullable=False, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    captainCode = Column(String, nullable=True, unique=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True)
    tasks = relationship("Tasks", back_populates="teams")
    members = relationship("Members", back_populates="teams")


class Members(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    discordName = Column(String, nullable=False)
    skillsets = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    teams = relationship("Teams", back_populates="members")
