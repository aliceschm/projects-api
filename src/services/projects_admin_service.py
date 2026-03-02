# Services related to projects table in the db
from src.infra.uow import UnitOfWork

from typing import List, Optional
from src.domain.schemas import ProjectCreate, ProjectStatus, ProjectOut, ProjectPatch
from src.domain.project_rules import (
    validate_deploy_date,
    validate_status,
    validate_project_publishable,
    validate_status_not_published,
)
from src.domain.exceptions import (
    ProjectNotFoundError,
    InvalidStatusError,
    ActionNotAllowedError,
    ProjectDescriptionNotFoundError,
    EmptyPatchError
)


# CRUD - PROJECT
# Create project
def create_project(uow: UnitOfWork, project: ProjectCreate):
    """Creates a new project. Returns the created project (as a schema / dict), not an ORM model."""
    validate_deploy_date(project.deploy_date)
    validate_status(project.status)
    validate_status_not_published(project.status)

    created = uow.projects.create(project)  # repo maps schema -> ORM internally
    uow.commit()
    uow.refresh(created)

    return ProjectOut.model_validate(created)


# Read projects
def read_all_projects(uow, lang: Optional[str] = None) -> List[ProjectOut]:
    """Returns list of projects. If lang is provided, returns desc in that language (if exists)."""
    projects = uow.projects.list_projects_admin(lang=lang)

    if not projects:
        raise ProjectNotFoundError("No projects found")
    

    return [ProjectOut.model_validate(p) for p in projects]


# # Read project
def read_project_by_id(
    uow: UnitOfWork, project_id: int, lang: Optional[str] = None
) -> ProjectOut:
    """Returns project details by slug. If lang is provided, returns desc in that language (if exists)."""
    project = uow.projects.get_by_id_admin(project_id=project_id, lang=lang)

    if not project:
        raise ProjectNotFoundError()
    
    if lang is not None and not project.descriptions:
        raise ProjectDescriptionNotFoundError()

    return ProjectOut.model_validate(project)

# Update project
def patch_project(uow: UnitOfWork, project_id: int, patch: ProjectPatch) -> ProjectOut:
    project = uow.projects.get_by_id_admin(project_id)
    if not project:
        raise ProjectNotFoundError()

    if project.status == ProjectStatus.PUBLISHED:
        raise ActionNotAllowedError("Published projects cannot be edited")

    # Empty patch
    if not patch.model_fields_set:
        raise EmptyPatchError()

    # Validate field only if they are in the payload
    if "deploy_date" in patch.model_fields_set:
        validate_deploy_date(patch.deploy_date)

    if "status" in patch.model_fields_set:
        validate_status_not_published(patch.status)
        validate_status(patch.status)


    #  apply patch, repo will handle mapping and applying changes to the ORM model
    uow.projects.apply_patch(project, patch)

    uow.commit()
    uow.refresh(project)

    return ProjectOut.model_validate(project)


# Delete project
def delete_project(uow: UnitOfWork, project_id: int):
    project = uow.projects.get_by_id_admin(project_id)

    if not project:
        raise ProjectNotFoundError()

    if project.status == ProjectStatus.PUBLISHED:
        raise ActionNotAllowedError()

    uow.projects.delete(project)
    uow.commit()


def publish_project(uow: UnitOfWork, project_id: int):
    project = uow.projects.get_by_id_admin(project_id=project_id)

    if not project:
        raise ProjectNotFoundError()

    if project.status == ProjectStatus.PUBLISHED:
        raise InvalidStatusError("Project is already published")

    validate_project_publishable(project)

    project.status = ProjectStatus.PUBLISHED

    uow.commit()
    uow.refresh(project)

    return ProjectOut.model_validate(project)
