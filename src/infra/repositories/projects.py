from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session, selectinload, with_loader_criteria

from src.domain.schemas import ProjectCreate, ProjectPatch, ProjectDescPatch
from src.infra.db import models


class ProjectsRepository:
    """
    Persistence-only operations for Projects aggregate.
    - No commit/rollback here (UnitOfWork controls transactions).
    - READ methods return ONLY ORM entities (SQLAlchemy models).
    """

    def __init__(self, db: Session):
        self.db = db

    # =========================================================
    # CRUD (session-level)
    # =========================================================

    def add(self, project: models.Projects) -> models.Projects:
        self.db.add(project)
        return project

    def delete(self, project: models.Projects) -> None:
        self.db.delete(project)

    def flush(self) -> None:
        self.db.flush()

    # =========================================================
    # CREATE (maps input -> ORM)
    # =========================================================

    def create(self, project_in: ProjectCreate) -> models.Projects:
        """
        Maps ProjectCreate (Pydantic) -> ORM and adds it to the session.
        UoW will commit/rollback.
        """
        db_project = models.Projects(
            status=project_in.status,
            slug=project_in.slug,
            deploy_date=project_in.deploy_date,
        )

        db_project.descriptions = [
            models.ProjectDesc(
                lang=d.lang,
                name=d.name,
                about=d.about,
                full_desc=d.full_desc,
            )
            for d in project_in.descriptions
        ]

        self.set_project_stacks(db_project, project_in.stacks)

        self.db.add(db_project)
        return db_project

    def slug_exists(self, slug: str) -> bool:
        return (
            self.db.query(models.Projects.id)
            .filter(models.Projects.slug == slug)
            .first()
            is not None
        )

    # =========================================================
    # READS (return ORM only)
    # =========================================================

    def list_projects_public(self, lang: Optional[str] = None) -> list[models.Projects]:
        return self._list_projects(public=True, lang=lang)

    def list_projects_admin(self, lang: Optional[str] = None) -> list[models.Projects]:
        return self._list_projects(public=False, lang=lang)

    def get_by_slug_public(self, slug: str, lang: Optional[str] = None) -> Optional[models.Projects]:
        return self._get_one(public=True, lang=lang, slug=slug)

    def get_by_id_admin(self, project_id: int, lang: Optional[str] = None) -> Optional[models.Projects]:
        return self._get_one(public=False, lang=lang, project_id=project_id)

    # =========================================================
    # MUTATIONS (operate on ORM)
    # =========================================================

    def apply_patch(self, project: models.Projects, patch: ProjectPatch) -> None:
        # Scalar fields
        for field in ("slug", "deploy_date", "status"):
            if field in patch.model_fields_set:
                setattr(project, field, getattr(patch, field))

        # Relationship updates
        if "descriptions" in patch.model_fields_set:
            self.set_project_descriptions(project, patch.descriptions or [])

        if "stacks" in patch.model_fields_set:
            self.set_project_stacks(project, patch.stacks or [])

        

    def set_project_descriptions(self, project: models.Projects, patches: list[ProjectDescPatch]) -> None:
        """
        Updates/creates descriptions by lang.
        Assumes `project.descriptions` is already loaded (we selectinload it in reads).
        """
        current_by_lang = {d.lang: d for d in (project.descriptions or [])}

        for p in patches:
            db_desc = current_by_lang.get(p.lang)

            if db_desc is None:
                # NOTE: keeping your original behavior; verify if FK should be project_id.
                db_desc = models.ProjectDesc(
                    id=project.id,
                    lang=p.lang,
                )
                project.descriptions.append(db_desc)
                current_by_lang[p.lang] = db_desc

            if "name" in p.model_fields_set:
                db_desc.name = p.name

            if "about" in p.model_fields_set:
                db_desc.about = p.about

            if "full_desc" in p.model_fields_set:
                db_desc.full_desc = p.full_desc

    def set_project_stacks(self, project: models.Projects, stack_names: list[str]) -> None:
        cleaned: list[str] = []
        seen: set[str] = set()

        for name in stack_names or []:
            raw = (name or "").strip()
            if not raw:
                continue

            normalized = raw.lower()
            if normalized in seen:
                continue

            seen.add(normalized)
            cleaned.append(raw)

        stack_objs = [self.get_or_create_stack(name) for name in cleaned]
        project.stacks = stack_objs

    def get_or_create_stack(self, stack_name: str) -> models.Stacks:
        normalized = stack_name.strip().lower()

        stack = (
            self.db.query(models.Stacks)
            .filter(models.Stacks.name_normalized == normalized)
            .first()
        )

        if stack is None:
            stack = models.Stacks(name=stack_name.strip(), name_normalized=normalized)
            self.db.add(stack)

        return stack

    # =========================================================
    # PRIVATE QUERY HELPERS (remove duplication)
    # =========================================================

    def _query_projects(self, *, public: bool, lang: Optional[str]):
        q = self.db.query(models.Projects).options(
            selectinload(models.Projects.descriptions),
            selectinload(models.Projects.stacks),
        )

        if public:
            q = q.filter(models.Projects.status == "published")

        if lang is not None:
            q = q.options(
                with_loader_criteria(
                    models.ProjectDesc,
                    models.ProjectDesc.lang == lang,
                    include_aliases=True,
                )
            )

        return q

    def _list_projects(self, *, public: bool, lang: Optional[str]) -> list[models.Projects]:
        return (
            self._query_projects(public=public, lang=lang)
            .order_by(models.Projects.deploy_date.desc())
            .all()
        )

    def _get_one(
        self,
        *,
        public: bool,
        lang: Optional[str],
        project_id: int | None = None,
        slug: str | None = None,
    ) -> Optional[models.Projects]:
        q = self._query_projects(public=public, lang=lang)

        if project_id is not None:
            q = q.filter(models.Projects.id == project_id)

        if slug is not None:
            q = q.filter(models.Projects.slug == slug)

        return q.first()