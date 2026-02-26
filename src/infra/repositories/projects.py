from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from src.domain.exceptions import UniqueConstraintError

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

    def delete(self, project) -> None:
        self.db.delete(project)

    def add(self, project) -> Optional[models.Projects]:
        self.db.add(project)
        return project

    def flush(self) -> None:
        self.db.flush()

    def get_or_create_stack(self, stack_name: str) -> models.Stacks:
        # Transform input to lowercase to compare to db lowercase column (name_normalize)
        normalized = stack_name.strip().lower()

        # Search in name_normalized column
        stack = (
            self.db.query(models.Stacks)
            .filter(models.Stacks.name_normalized == normalized)
            .first()
        )

        if not stack:
            stack = models.Stacks(name=stack_name.strip(), name_normalized=normalized)
            self.db.add(stack)

        return stack

    def set_project_stacks(
        self, project: models.Projects, stack_names: list[str]
    ) -> None:
        cleaned = []
        seen = set()

        for name in stack_names or []:
            if not name or not name.strip():
                continue
            raw = name.strip()
            normalized = raw.lower()
            if normalized in seen:
                continue
            seen.add(normalized)
            cleaned.append(raw)

            stack_objs = [self.get_or_create_stack(name) for name in cleaned]
            project.stacks = stack_objs


class UnitOfWork:
    """
    One UnitOfWork per request.
    Holds the DB session + repositories and controls commit/rollback.
    """

    def __init__(self, db: Session):
        self.db = db
        self.projects = ProjectsRepository(db)

    def rollback(self) -> None:
        self.db.rollback()

    def refresh(self, instance) -> None:
        self.db.refresh(instance)

    def commit(self) -> None:
        try:
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()

            diag = getattr(getattr(e, "orig", None), "diag", None)
            constraint_name = getattr(diag, "constraint_name", None)
            print(
                f"IntegrityError in UnitOfWork.commit: {e}, constraint: {constraint_name}"
            )

            raise UniqueConstraintError(constraint=constraint_name) from e
