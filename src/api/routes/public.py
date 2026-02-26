# All public endpoints related to projects - no auth required

from fastapi import APIRouter, Depends, status, Query
from typing import List, Annotated
from src.domain.schemas import ProjectLang, ProjectOut, ProjectDetailOut
from src.services import projects_service

from src.infra.uow import UnitOfWork
from src.api.dependencies import get_uow

router = APIRouter(prefix="/projects", tags=["Projects (Public)"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ProjectOut])
def read_all_projects(
    uow: Annotated[UnitOfWork, Depends(get_uow)], lang: ProjectLang | None = Query(default=None)
):
    return projects_service.read_all_projects(uow, lang)


# read project
@router.get(
    "/{project_slug}", status_code=status.HTTP_200_OK, response_model=ProjectDetailOut
)
def read_project(
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    project_slug: str,
    lang: ProjectLang | None = Query(default=None),
):
    return projects_service.read_project_by_slug(
        uow=uow,
        slug=project_slug,
        lang=lang,
    )
