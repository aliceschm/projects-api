# All admin endpoints related to projects - auth required

from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from typing import Annotated
from src.database import get_db
from src.schemas import ProjectCreate, ProjectPatch
from src.services import projects_service
from src.auth.dependencies import require_api_key

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/projects", tags=["Projects (Admin)"], dependencies=[Depends(require_api_key)])

#create project
@router.post("/", status_code = status.HTTP_201_CREATED)
def create_project(db: db_dependency, project: ProjectCreate, response: Response):
    new_project = projects_service.create_project(db, project)
    response.headers["Location"] = f"/projects/{new_project.id}"
    return new_project

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

#publish project
@router.post("/{project_id}/publish", status_code=status.HTTP_200_OK)
def publish_project(db: db_dependency,project_id: int,response: Response):
    published_project = projects_service.publish_project(db, project_id)
    response.headers["Location"] = f"/projects/{published_project.id}"
    return published_project
