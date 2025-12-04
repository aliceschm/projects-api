# Services related to projects table in the db
from sqlalchemy.orm import Session
from datetime import datetime
from src import models
from src.schemas import ProjectCreate, ProjectDescPatch, ProjectPatch
from src.services.stacks_service import get_or_create_stack, update_project_stacks
from src.services.project_desc_service import update_project_desc
from fastapi import HTTPException

# CRUD - PROJECT
# Create_project
def create_project(project: ProjectCreate, db: Session):
    """
    Service layer:
    - Router injects the DB session
    - Service receives the session and performs all DB work
    """

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
            project_id=db_project.id,
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
def read_all_projects(db :Session):
    projects = db.query(models.ProjectView).all()
    return projects

# Read project
def read_project(project_id: int, db: Session):
    project = db.query(models.ProjectView).filter(models.ProjectView.id == project_id).first()
    return project

# Update projects table
def update_project_base(db, project, patch):
    data = patch.model_dump(exclude_unset=True)

    for field in ("status", "slug", "deploy_date"):
        if field in data:
            setattr(project, field, data[field])

    db.flush()

# Update project

def patch_project(project_id: int, patch: ProjectPatch, db: Session):
    project = (
        db.query(models.Projects)
          .filter(models.Projects.id == project_id)
          .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Update main table
    update_project_base(db, project, patch)

    # Update description: create/update/remove
    if patch.description is not None:
        update_project_desc(db, project_id, patch.description)

    # Update stacks
    if patch.stacks is not None:
        update_project_stacks(db, project_id, patch.stacks)

    db.commit()
    db.refresh(project)

    updated_project = (
        db.query(models.ProjectView)
          .filter(models.ProjectView.id == project_id)
          .first()
    )
    return updated_project
