# All public endpoints related to projects - no auth required

from fastapi import APIRouter, Depends, status
from typing import List, Annotated
from src.domain.schemas import ProjectOut, ProjectDetailOut
from src.services import projects_service
from src.domain.language import get_language
from src.infra.uow import UnitOfWork
from src.api.dependencies import get_uow

router = APIRouter(prefix="/projects", tags=["Projects (Public)"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ProjectOut])
def read_all_projects(
    uow: Annotated[UnitOfWork, Depends(get_uow)], lang: str = Depends(get_language)
):
    result_projects = projects_service.read_all_projects(uow, lang)
    return result_projects


# read project
@router.get(
    "/{project_id}", status_code=status.HTTP_200_OK, response_model=ProjectDetailOut
)
def read_project(
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    project_id: int,
    lang: str = Depends(get_language),
):
    result_project = projects_service.read_project_by_id(uow, project_id, lang)
    return result_project
