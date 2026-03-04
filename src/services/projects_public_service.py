# Services related to projects table in the db
from src.infra.uow import UnitOfWork

from typing import List, Optional
from src.domain.schemas import ProjectOut

from src.domain.exceptions import ProjectNotFoundError, ProjectDescriptionNotFoundError


# Read projects
def read_all_projects(
    uow, lang: Optional[str] = None, limit: int = 50, offset: int = 0
) -> List[ProjectOut]:
    """Returns list of projects. If lang is provided, returns desc in that language (if exists)."""
    projects = uow.projects.list_projects_public(lang=lang, limit=limit, offset=offset)

    if not projects:
        raise ProjectNotFoundError("No projects found")

    return [ProjectOut.model_validate(p) for p in projects]


# # Read project
def read_project_by_slug(
    uow: UnitOfWork, slug: str, lang: Optional[str] = None
) -> ProjectOut:
    """Returns project details by slug. If lang is provided, returns desc in that language (if exists)."""
    project = uow.projects.get_by_slug_public(slug=slug, lang=lang)

    if not project:
        raise ProjectNotFoundError()

    if lang is not None and not project.descriptions:
        raise ProjectDescriptionNotFoundError()

    return ProjectOut.model_validate(project)


#
