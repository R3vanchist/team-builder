from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Post(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class Teams(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    gitRepo = Column(String, nullable=True)
    location = Column(String, nullable=False)
    preferredWorkTime = Column(String, nullable=False)
    classificationLevel = Column(String, nullable=False)
    preferredSkillsets = Column(String, nullable=False)
    needsMembers = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    captainCode = Column(String, nullable=True, unique=True)
    taskId = Column(Integer, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True)


class Members(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    skillsets = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    teamId = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=True)
