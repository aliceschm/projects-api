# All endpoints related to projects

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Annotated
import datetime
from src import models
from src.database import get_db
from src.schemas import ProjectCreate, ProjectOut
from src.services import project_service

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/projects", tags=["Projects"])

#create project
@router.post("/")
def create_project(project: ProjectCreate, db: db_dependency):
    new_project = project_service.create_project(project, db)
    return new_project

#read projects
@router.get("/", response_model=List[ProjectOut])
def read_all_projects(db: db_dependency):
   result_projects = project_service.read_all_projects(db)
   return result_projects

#read project
@router.get("/{project_id}")
def read_project(project_id: int, db: db_dependency):
    result_project = project_service.read_project(project_id, db)
    return result_project

