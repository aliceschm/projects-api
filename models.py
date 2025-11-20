from sqlalchemy import Text, CheckConstraint, Date, Column, ForeignKey, Integer, PrimaryKeyConstraint, TIMESTAMP, ARRAY, JSONB
from database import Base
from datetime import datetime


class Projects(Base):
    __tablename__ = 'projects'
    __table_args__ = (
        CheckConstraint("status IN ('idea', 'planning', 'in_progress', 'paused', 'finished', 'archived')",
                        name="status_check"),
        {"schema": "portfolio"},
    )

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now)
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now)
    status = Column(Text, nullable=False, server_default="idea")
    slug = Column(Text, nullable=False)

class ProjectDesc(Base):
    __tablename__ = "project_desc"
    __table_args__ = (
        PrimaryKeyConstraint("project_id", "lang"),
        CheckConstraint("lang IN ('pt', 'en', 'es')", name="lang_check"),
        {"schema": "portfolio"},
    )

    project_id = Column(Integer, ForeignKey("portfolio.projects.id", ondelete="CASCADE"))
    name = Column(Text, nullable=False, server_default="")
    about = Column(Text)
    full_desc = Column(Text)
    lang = Column(Text, nullable=False, server_default="pt")

class Stacks(Base):
    __tablename__ = 'stacks'
    __table_args__ = {"schema": "portfolio"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)

class ProjectStack(Base):
    __tablename__ = 'project_stack'
    __table_args__ = (
        PrimaryKeyConstraint("project_id", "stack_id"),
        {"schema": "portfolio"},
    )

    project_id = Column(Integer, ForeignKey("portfolio.projects.id", ondelete="CASCADE"))
    stack_id = Column(Integer, ForeignKey("portfolio.stacks.id"))

class ProjectView(Base):
    __tablename__ = "project_view"
    __table_args__ = {"schema": "portfolio"}

    # Precisa marcar a PK lógica
    id = Column(Integer, primary_key=True)

    date = Column(TIMESTAMP)
    status = Column(Text)

    stack_ids = Column(ARRAY(Integer))
    stack_names = Column(ARRAY(Text))

    translations = Column(JSONB)