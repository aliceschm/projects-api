from __future__ import annotations

from sqlalchemy.orm import Session
from typing import Optional

from src import models


class ProjectsRepository:
    """
    Persistence-only operations for Projects aggregate.
    No commit/rollback here (UnitOfWork controls transactions).
    """

    def __init__(self, db: Session):
        self.db = db

    def get(self, project_id: int) -> Optional[models.Projects]:
        return (
            self.db.query(models.Projects)
            .filter(models.Projects.id == project_id)
            .first()
        )


class UnitOfWork:
    """
    One UnitOfWork per request.
    Holds the DB session + repositories and controls commit/rollback.
    """

    def __init__(self, db: Session):
        self.db = db
        self.projects = ProjectsRepository(db)

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()

    def refresh(self, instance) -> None:
        self.db.refresh(instance)