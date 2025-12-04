# All endpoints related to projects

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Annotated
import datetime
from src import models
from src.database import get_db
from src.schemas import ProjectCreate, ProjectOut, ProjectPatch
from src.services import projects_service

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/projects", tags=["Projects"])

#create project
@router.post("/", status_code = status.HTTP_201_CREATED)
def create_project(project: ProjectCreate, db: db_dependency):
    new_project = projects_service.create_project(project, db)
    return new_project

#read projects
@router.get("/", status_code = status.HTTP_200_OK, response_model = List[ProjectOut])
def read_all_projects(db: db_dependency):
   result_projects = projects_service.read_all_projects(db)
   return result_projects

#read project
@router.get("/{project_id}", status_code = status.HTTP_200_OK, response_model = ProjectOut)
def read_project(project_id: int, db: db_dependency):
    result_project = projects_service.read_project(project_id, db)
    return result_project

#update project
@router.patch("/{project_id}", status_code = status.HTTP_200_OK)
def patch_project(project_id: int, patch: ProjectPatch, db: db_dependency):
    updated_project = projects_service.patch_project(project_id, patch, db)
    return updated_project

#delete project
@router.delete("/{project_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: db_dependency):
    projects_service.delete_project(project_id, db)
