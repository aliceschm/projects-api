from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import models
from typing import List, Annotated, Optional
import datetime
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from enum import Enum

app = FastAPI()

class LangEnum(str, Enum):
    pt = "pt"
    en = "en"
    es = "es"

#table schemas
class ProjectBase(BaseModel):
    name: str
    about: Optional[str] = None
    full_desc: Optional[str] = None
    date: Optional[datetime.date] = None
    lang: LangEnum = LangEnum.pt
    status: Optional[str] = None
    stacks: list[int] = [] 
    

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/projects")
async def create_projects(project:ProjectBase, db:db_dependency):
    db_project = models.Projects(
        name=project.name,
        about=project.about,
        full_desc=project.full_desc,
        date=project.date,
        lang=project.lang,
        status=project.status)
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    for stack_id in project.stacks:
        relation = models.Project_stack(
            project_id=db_project.id,
            stack_id=stack_id
        )
        db.add(relation)

    db.commit()
    return {"message": "Project created", "id": db_project.id}