# All public endpoints related to projects - no auth required

from fastapi import APIRouter, Depends, status, Query, Request
from typing import List, Annotated
from src.domain.schemas import ProjectLang, ProjectOut
from src.services import projects_public_service

from src.infra.uow import UnitOfWork
from src.api.dependencies import get_uow
from src.api.limiter import limiter

router = APIRouter(prefix="/projects", tags=["Projects (Public)"])

DEFAULT_LIMIT = 20
MAX_LIMIT = 50


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[ProjectOut],
    summary="List published projects",
    description="Returns a list of published projects. Optional query parameters for pagination (limit, offset) and language-specific descriptions (lang).",
)
@limiter.limit("30/minute")
def read_all_projects(
    request: Request,
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    lang: Annotated[ProjectLang | None, Query()] = None,
    limit: int = Query(
        default=DEFAULT_LIMIT,
        ge=1,
        le=MAX_LIMIT,
        description="Maximum number of projects to return.",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Number of projects to skip before starting to collect the result set (pagination).",
    ),
):
    return projects_public_service.read_all_projects(
        uow=uow, lang=lang, limit=limit, offset=offset
    )


@router.get(
    "/{project_slug}",
    status_code=status.HTTP_200_OK,
    response_model=ProjectOut,
    summary="Get published project by slug",
    description="Returns details of a published project identified by its slug. Optional query parameter for language-specific description (lang).",
)
@limiter.limit("30/minute")
def read_project(
    request: Request,
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    project_slug: str,
    lang: Annotated[ProjectLang | None, Query()] = None,
):
    return projects_public_service.read_project_by_slug(
        uow=uow,
        slug=project_slug,
        lang=lang,
    )
