# All endpoints related to projects

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Annotated
import datetime
from src import models
from src.database import get_db
from src.schemas import ProjectCreate
from src.services import project_service

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/projects", tags=["Projects"])

#CRUD - PROJECT
#create project
@router.post("/")
def create_project(project: ProjectCreate, db: db_dependency):
    new_project = project_service.create_project(project, db)
    return new_project

# #read project
# @router.get("/{project_id}")
# def read_project(db: db_dependency, project_id: int):
#     result_project = project_service.read_project(db, project_id)
#     return result_project

# @router.get("/", response_model=List[ProjectBase])
# def read_all_projects(db: db_dependency):
#    result_projects = project_service.read_all_projects(db)
#    return result_projects

