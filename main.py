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

# pydantic model used for request validation and structure
class ProjectBase(BaseModel):
    name: str
    about: Optional[str] = None
    full_desc: Optional[str] = None
    date: Optional[datetime.date] = None
    lang: LangEnum = LangEnum.pt
    status: Optional[str] = None
    stacks: list[int] = [] 
    

# dependency that creates and closes a db session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/projects", response_model=list[ProjectBase]) # pydantic response_model to convert result to json
async def get_all_projects(db:db_dependency):
    # fetch all projects from database
    result = db.query(models.Projects).all()
    if not result:
        raise HTTPException(status_code=404, detail="No projects found.")
    return result

@app.get("/projects/{project_id}")
async def get_project(project_id: int, db:db_dependency):
    result = db.query(models.Projects).filter(models.Projects.id == project_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Project not found.")
    return result

@app.post("/projects")
async def create_projects(project:ProjectBase, db:db_dependency):
    # create project using validated pydantic data
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