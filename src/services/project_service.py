# All project services
from sqlalchemy.orm import Session
from datetime import datetime
from src import models
from src.schemas import ProjectCreate
from src.services.stack_service import get_or_create_stack

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
def read_all_projects(db:Session):
    projects = db.query(models.ProjectView).all()
    return projects
