# All public endpoints related to projects - no auth required

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Annotated
from src.database import get_db
from src.schemas import ProjectOut, ProjectOut, ProjectDetailOut
from src.services import projects_service
from src.domain.language import get_language

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/projects", tags=["Projects (Public)"])


@router.get("/", status_code = status.HTTP_200_OK, response_model = List[ProjectOut])
def read_all_projects(db: db_dependency, lang: str = Depends(get_language)):
   result_projects = projects_service.read_all_projects(db, lang)
   return result_projects

#read project
@router.get("/{project_id}", status_code = status.HTTP_200_OK, response_model = ProjectDetailOut)
def read_project(db: db_dependency, project_id: int, lang: str = Depends(get_language)):
    result_project = projects_service.read_project_by_id(db, project_id, lang)
    return result_project

