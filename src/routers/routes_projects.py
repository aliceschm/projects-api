# All endpoints related to projects

from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from typing import List, Annotated
from src.database import get_db
from src.schemas import ProjectCreate, ProjectOut, ProjectPatch, ProjectOut, ProjectDetailOut
from src.services import projects_service
from src.domain.language import get_language

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/projects", tags=["Projects"])

#create project
@router.post("/", status_code = status.HTTP_201_CREATED)
def create_project(db: db_dependency, project: ProjectCreate, response: Response):
    new_project = projects_service.create_project(db, project)
    response.headers["Location"] = f"/projects/{new_project.id}"
    return new_project

#read projects
@router.get("/", status_code = status.HTTP_200_OK, response_model = List[ProjectOut])
def read_all_projects(db: db_dependency, lang: str = Depends(get_language)):
   result_projects = projects_service.read_all_projects(db, lang)
   return result_projects

#read project
@router.get("/{project_id}", status_code = status.HTTP_200_OK, response_model = ProjectDetailOut)
def read_project(db: db_dependency, project_id: int, lang: str = Depends(get_language)):
    result_project = projects_service.read_project_by_id(db, project_id, lang)
    return result_project

#update project
@router.patch("/{project_id}", status_code = status.HTTP_200_OK)
def patch_project(db: db_dependency, project_id: int, patch: ProjectPatch, response: Response):
    updated_project = projects_service.patch_project(db, project_id, patch)
    response.headers["Location"] = f"/projects/{updated_project.id}"
    return updated_project

#delete project
@router.delete("/{project_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_project(db: db_dependency, project_id: int):
    projects_service.delete_project(db, project_id)
