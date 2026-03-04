# All public endpoints related to projects - no auth required

from fastapi import APIRouter, Depends, status, Query, Request
from typing import List, Annotated
from src.domain.schemas import ProjectLang, ProjectOut
from src.services import projects_public_service

from src.infra.uow import UnitOfWork
from src.api.dependencies import get_uow
from src.api.limiter import limiter

router = APIRouter(prefix="/projects", tags=["Projects (Public)"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ProjectOut])
@limiter.limit("30/minute")
def read_all_projects(
    request: Request,
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    lang: ProjectLang | None = Query(default=None),
):
    return projects_public_service.read_all_projects(uow, lang)


@router.get(
    "/{project_slug}", status_code=status.HTTP_200_OK, response_model=ProjectOut
)
@limiter.limit("30/minute")
def read_project(
    request: Request,
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    project_slug: str,
    lang: ProjectLang | None = Query(default=None),
):
    return projects_public_service.read_project_by_slug(
        uow=uow,
        slug=project_slug,
        lang=lang,
    )
