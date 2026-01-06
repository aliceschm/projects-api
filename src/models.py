# Defines SQLAlchemy ORM models representing database tables.
# These classes allow interaction with the database using Python objects instead of raw SQL.

from sqlalchemy import Text, CheckConstraint, Date, Column, ForeignKey, Integer, PrimaryKeyConstraint, TIMESTAMP, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from src.database import Base
from datetime import datetime

class Projects(Base):
    __tablename__ = 'projects'
    __table_args__ = (
        CheckConstraint("status IN ('idea', 'planning', 'in_progress', 'paused', 'finished', 'archived', 'published')",
                        name="status_check"),
        {"schema": "portfolio"},
    )

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now)
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    status = Column(Text, nullable=False, server_default="idea")
    slug = Column(Text, nullable=False)
    deploy_date = Column(Date, nullable=True)

    descriptions = relationship("ProjectDesc",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    stacks = relationship(
        "Stacks",
        secondary="portfolio.project_stack",
        back_populates="projects",
        lazy="selectin",
    )

class ProjectDesc(Base):
    __tablename__ = "project_desc"
    __table_args__ = (
        PrimaryKeyConstraint("id", "lang"),
        CheckConstraint("lang IN ('pt', 'en', 'es')", name="lang_check"),
        {"schema": "portfolio"},
    )

    id = Column(Integer, ForeignKey("portfolio.projects.id", ondelete="CASCADE"))
    name = Column(Text, nullable=False, server_default="")
    about = Column(Text)
    full_desc = Column(Text)
    lang = Column(Text, nullable=False, server_default="pt")

    project = relationship(
        "Projects",
        back_populates="descriptions",
        lazy= "selectin"
    )

class Stacks(Base):
    __tablename__ = 'stacks'
    __table_args__ = {"schema": "portfolio"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    name_normalized = Column(Text, nullable=False)

    projects = relationship(
        "Projects",
        secondary="portfolio.project_stack",
        back_populates="stacks",
        lazy="selectin",
    )



class ProjectStack(Base):
    __tablename__ = 'project_stack'
    __table_args__ = (
        PrimaryKeyConstraint("project_id", "stack_id"),
        {"schema": "portfolio"},
    )

    project_id = Column(Integer, ForeignKey("portfolio.projects.id", ondelete="CASCADE"))
    stack_id = Column(Integer, ForeignKey("portfolio.stacks.id"))
