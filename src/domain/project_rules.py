from datetime import date
from sqlalchemy.orm import Session
from src import models
from src.domain.exceptions import (
    InvalidDeployDateError,
    InvalidStatusError,
    SlugAlreadyExistsError,
    ProjectNotPublishableError,
)
from src.schemas import ProjectLang, ProjectStatus


REQUIRED_LANGS = {lang.value for lang in ProjectLang}
REQUIRED_DESC_FIELDS = {"name", "about", "full_desc"}


def validate_deploy_date(deploy_date):
    if deploy_date and deploy_date > date.today():
        raise InvalidDeployDateError()


def validate_slug_unique(db: Session, slug: str, project_id: int | None = None):
    # validate if slug exists in project create and project patch
    query = db.query(models.Projects).filter(models.Projects.slug == slug)

    if project_id:
        query = query.filter(models.Projects.id != project_id)

    if query.first():
        raise SlugAlreadyExistsError()


def validate_status(status, allowed):
    if status not in allowed:
        raise InvalidStatusError()


def validate_project_publishable(project):
    errors = []

    if not project.deploy_date:
        errors.append("deploy_date is required for published projects")

    if not project.stacks:
        errors.append("at least one stack is required for published projects")

    desc_by_lang = {d.lang: d for d in project.descriptions}
    missing_langs = REQUIRED_LANGS - desc_by_lang.keys()

    if missing_langs:
        errors.append(f"missing descriptions for languages: {missing_langs}")

    for lang in REQUIRED_LANGS:
        desc = desc_by_lang.get(lang)
        if not desc:
            continue

        for field in REQUIRED_DESC_FIELDS:
            if not getattr(desc, field):
                errors.append(
                    f"description field '{field}' is required for language '{lang}'"
                )

    if errors:
        raise ProjectNotPublishableError("; ".join(errors))


def validate_status_not_published(status):
    if status == ProjectStatus.PUBLISHED:
        raise InvalidStatusError(
            "published status is only allowed via publish endpoint"
        )
