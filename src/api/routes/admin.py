# All admin endpoints related to projects - auth required

from fastapi import APIRouter, Depends, status, Response, Query
from typing import Annotated, List
from src.domain.schemas import ProjectCreate, ProjectPatch, ProjectLang, ProjectOut
from src.services import projects_admin_service
from src.auth.dependencies import require_api_key
from src.infra.uow import UnitOfWork
from src.api.dependencies import get_uow

router = APIRouter(
    prefix="/admin/projects",
    tags=["Projects (Admin)"],
    dependencies=[Depends(require_api_key)],
)


# create project
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_project(
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    project: ProjectCreate,
    response: Response,
):
    new_project = projects_admin_service.create_project(uow, project)
    response.headers["Location"] = f"/projects/{new_project.id}"
    return new_project


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ProjectOut])
def read_all_projects(
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    lang: ProjectLang | None = Query(default=None),
):
    return projects_admin_service.read_all_projects(uow, lang)


# read project
@router.get(
    "/{project_id}", status_code=status.HTTP_200_OK, response_model=ProjectOut
)
def read_project(
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    project_id: int,
    lang: ProjectLang | None = Query(default=None),
):
    return projects_admin_service.read_project_by_id(
        uow=uow,
        project_id=project_id,
        lang=lang,
    )


# update project
@router.patch("/{project_id}", status_code=status.HTTP_200_OK)
def patch_project(
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    project_id: int,
    patch: ProjectPatch,
    response: Response,
):
    updated_project = projects_admin_service.patch_project(uow, project_id, patch)
    response.headers["Location"] = f"/projects/{updated_project.id}"
    return updated_project


# delete project
@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(uow: Annotated[UnitOfWork, Depends(get_uow)], project_id: int):
    projects_admin_service.delete_project(uow, project_id)


# publish project
@router.post("/{project_id}/publish", status_code=status.HTTP_200_OK)
def publish_project(
    uow: Annotated[UnitOfWork, Depends(get_uow)], project_id: int, response: Response
):
    published_project = projects_admin_service.publish_project(uow, project_id)
    response.headers["Location"] = f"/projects/{published_project.id}"
    return published_project
