# Services related to projects table in the db
from src.infra.uow import UnitOfWork
from sqlalchemy.orm import Session, joinedload
from src.infra.db import models
from src.domain.schemas import (
    ProjectCreate,
    ProjectPatch,
    ProjectStatus,
    ProjectOut,
    ProjectDetailOut,
)
from src.services.project_desc_service import update_project_desc
from src.domain.project_rules import (
    validate_deploy_date,
    validate_status,
    validate_project_publishable,
    validate_status_not_published,
)
from src.domain.exceptions import (
    ProjectNotFoundError,
    EmptyPatchError,
    InvalidStatusError,
    ProjectDeleteNotAllowedError,
)


# CRUD - PROJECT
# Create project
def create_project(uow: UnitOfWork, project: ProjectCreate):
    """Creates a new project. Returns the created project."""
    validate_deploy_date(project.deploy_date)
    validate_status(project.status, ProjectStatus)
    validate_status_not_published(project.status)

    db_project = models.Projects(
        status=project.status,
        slug=project.slug,
        deploy_date=project.deploy_date,
    )

    db_project.descriptions = [
        models.ProjectDesc(
            lang=desc.lang,
            name=desc.name,
            about=desc.about,
            full_desc=desc.full_desc,
        )
        for desc in project.descriptions
    ]

    uow.projects.set_project_stacks(db_project, project.stacks)

    uow.projects.add(db_project)
    uow.commit()

    return db_project


# Read projects
def read_all_projects(db: Session, lang: str = "pt"):
    projects = (
        db.query(models.Projects)
        .filter(models.Projects.status == "published")
        .options(
            joinedload(models.Projects.descriptions),
            joinedload(models.Projects.stacks),
        )
        .all()
    )

    projects_list = []

    for project in projects:
        desc = next((d for d in project.descriptions if d.lang == lang), None)

        if not desc:
            continue

        projects_list.append(
            ProjectOut(
                id=project.id,
                slug=project.slug,
                name=desc.name,
                about=desc.about,
                stack_names=[stack.name for stack in project.stacks],
            )
        )

    return projects_list


# Read project
def read_project_by_id(db: Session, project_id: int, lang: str):
    project = (
        db.query(models.Projects)
        .filter(models.Projects.status == "published")
        .options(
            joinedload(models.Projects.descriptions), joinedload(models.Projects.stacks)
        )
        .filter(models.Projects.id == project_id)
        .first()
    )

    if not project:
        raise ProjectNotFoundError()

    # Get desc in the requested language
    desc = next((d for d in project.descriptions if d.lang == lang), None)

    return ProjectDetailOut(
        id=project.id,
        lang=lang,
        slug=project.slug,
        deploy_date=project.deploy_date,
        status=project.status,
        stack_names=[stack.name for stack in project.stacks] if project.stacks else [],
        full_desc=desc.full_desc if desc and desc.full_desc else None,
    )


# Update project (partial)
def patch_project(db: Session, project_id: int, patch: ProjectPatch):
    project = db.query(models.Projects).filter(models.Projects.id == project_id).first()

    if not project:
        raise ProjectNotFoundError()

    data = patch.model_dump(exclude_unset=True)
    data = {k: v for k, v in data.items() if v is not None}

    if not data and patch.descriptions is None and patch.stacks is None:
        raise EmptyPatchError()

    # Logic validations
    if patch.deploy_date is not None:
        validate_deploy_date(patch.deploy_date)

    if patch.status is not None:
        validate_status(patch.status, ProjectStatus)
        validate_status_not_published(patch.status)

    content_changed = False

    # Update main table
    for field in ("slug", "deploy_date"):
        if field in data and getattr(project, field) != data[field]:
            setattr(project, field, data[field])
            content_changed = True

    # Update descriptions
    if patch.descriptions is not None:
        update_project_desc(db, project_id, patch.descriptions)
        content_changed = True

    # Update stacks
    if patch.stacks is not None:
        update_project_stacks(db, project_id, patch.stacks)
        content_changed = True

    # Force draft only if something really changed
    if project.status == ProjectStatus.PUBLISHED and content_changed:
        project.status = ProjectStatus.DRAFT

    db.commit()

    return project


# Delete project
def delete_project(uow: UnitOfWork, project_id: int):
    project = uow.projects.get(project_id)

    if not project:
        raise ProjectNotFoundError()

    if project.status == ProjectStatus.PUBLISHED:
        raise ProjectDeleteNotAllowedError()

    uow.delete(project)
    uow.commit()


def publish_project(uow: UnitOfWork, project_id: int):
    project = uow.projects.get(project_id)

    if not project:
        raise ProjectNotFoundError()

    if project.status == ProjectStatus.PUBLISHED:
        raise InvalidStatusError("Project is already published")

    validate_project_publishable(project)

    project.status = ProjectStatus.PUBLISHED

    uow.commit()
    uow.refresh(project)

    return project
