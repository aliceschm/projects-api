from __future__ import annotations


from sqlalchemy.orm import Session
from typing import Optional

from src.infra.db import models


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

