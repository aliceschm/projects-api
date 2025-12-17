# Services related to projects table in the db
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from src import models
from src.schemas import ProjectCreate, ProjectDescPatch, ProjectPatch, ProjectStatus, ProjectOut, ProjectDetailOut
from src.services.stacks_service import get_or_create_stack, update_project_stacks
from src.services.project_desc_service import update_project_desc
from fastapi import HTTPException
from src.domain.project_validations import validate_deploy_date, validate_slug_unique, validate_status


# CRUD - PROJECT
# Create project
def create_project(db: Session, project: ProjectCreate):
    """
    Service layer:
    - Router injects the DB session
    - Service receives the session and performs all DB work
    """

    #Logic validations
    validate_deploy_date(project.deploy_date)
    validate_slug_unique(db, project.slug)
    validate_status(project.status, ProjectStatus)

    # Create the project record
    db_project = models.Projects(
        created_at=datetime.now(),
        updated_at=datetime.now(),
        status=project.status,
        slug=project.slug,
        deploy_date=project.deploy_date
    )

    db.add(db_project)
    db.flush()  # ensure db_project.id exists

    # Insert multiple descriptions
    for desc in project.descriptions:
        db_desc = models.ProjectDesc(
            id=db_project.id,
            lang=desc.lang,
            name=desc.name,
            about=desc.about,
            full_desc=desc.full_desc
        )
        db.add(db_desc)

    #Insert stacks
    for stack_name in project.stacks:
        stack = get_or_create_stack(db, stack_name)
        proj_stack = models.ProjectStack(
            project_id=db_project.id,
            stack_id=stack.id
        )
        db.add(proj_stack)

    # Commit everything
    db.commit()
    db.refresh(db_project)

    return db_project

# Read projects
def read_all_projects(db: Session, lang: str = "pt"):
    projects = (
        db.query(models.Projects)
        .options(
            joinedload(models.Projects.descriptions),
            joinedload(models.Projects.stacks),
        )
        .all()
    )

    projects_list = []

    for project in projects:
        desc = next(
            (d for d in project.descriptions if d.lang == lang),
            None
        )

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
        .options(
            joinedload(models.Projects.descriptions),
            joinedload(models.Projects.stacks)
        )
        .filter(models.Projects.id == project_id)
        .first()
    )

    if not project:
        return None  # ou raise HTTPException(status_code=404, ...)

    # Pega a descrição no idioma solicitado
    desc = next((d for d in project.descriptions if d.lang == lang), None)

    return ProjectDetailOut(
        id=project.id,
        lang=lang,
        slug=project.slug,
        deploy_date=project.deploy_date,
        status=project.status,
        stack_names=[stack.name for stack in project.stacks] if project.stacks else [],
        full_desc=desc.full_desc if desc and desc.full_desc else None
    )

# Update projects table
def update_project_base(db: Session, project, patch):
    data = patch.model_dump(exclude_unset=True)

    for field in ("status", "slug", "deploy_date"):
        if field in data:
            setattr(project, field, data[field])

    db.flush()

# Update project (partial)
def patch_project(db: Session, project_id: int, patch: ProjectPatch):
    project = db.query(models.Projects).filter(models.Projects.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
  
    # Logic validations
    if patch.deploy_date is not None:
        validate_deploy_date(patch.deploy_date)

    if patch.status is not None:
        validate_status(patch.status, ProjectStatus)

    if patch.slug is not None:
        validate_slug_unique(db, patch.slug)

    # Update description: create/update/remove
    if patch.description is not None:
        update_project_desc(db, project_id, patch.description)

    # Update main table
    update_project_base(db, project, patch)
    
    # Update stacks
    if patch.stacks is not None:
        update_project_stacks(db, project_id, patch.stacks)

    db.commit()
    db.refresh(project)

    return project

# Delete project
def delete_project(db: Session, project_id: int):
    project = (
        db.query(models.Projects)
          .filter(models.Projects.id == project_id)
          .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()
