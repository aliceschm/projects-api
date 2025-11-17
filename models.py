from sqlalchemy import Text, CheckConstraint, Date, Column, ForeignKey, Integer, PrimaryKeyConstraint
from database import Base


class Projects(Base):
    __tablename__ = 'projects'
    __table_args__ = (
        CheckConstraint("lang IN ('pt', 'en', 'es')"),
        {"schema": "portfolio"},
    )

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(Text, nullable=False, server_default="", index=True)
    about = Column(Text)
    full_desc = Column(Text)
    date = Column(Date)
    lang = Column(Text, nullable=False, server_default="pt")
    status = Column(Text)

class Stacks(Base):
    __tablename__ = 'stacks'
    __table_args__ = {"schema": "portfolio"}

    id= Column(Integer, primary_key=True, autoincrement=True, index=True)
    name= Column(Text, nullable=False)

class Project_stack(Base):
    __tablename__ = 'project_stack'
    __table_args__ = (
        PrimaryKeyConstraint("project_id", "stack_id"),
        {"schema": "portfolio"},
    )

    project_id = Column(Integer, ForeignKey("portfolio.projects.id"))
    stack_id = Column(Integer, ForeignKey("portfolio.stacks.id"))


