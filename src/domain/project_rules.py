from typing import Optional
from datetime import date
from src.domain.exceptions import (
    InvalidDeployDateError,
    InvalidStatusError,
    ProjectNotPublishableError,
)
from src.domain.schemas import ProjectLang, ProjectOut, ProjectStatus


REQUIRED_LANGS = {lang.value for lang in ProjectLang}
REQUIRED_DESC_FIELDS = {"name", "about", "full_desc"}


def validate_deploy_date(deploy_date: Optional[date]) -> None:
    if deploy_date is None:
        return
    
    if deploy_date > date.today():
        raise InvalidDeployDateError()


def validate_status(status: Optional[ProjectStatus]) -> None: # Pydantic will validate missing or invalid status, no exception handler neeed 
    if status is None:
        return 


def validate_project_publishable(project: ProjectOut) -> None:
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


def validate_status_not_published(status: ProjectStatus) -> None:
    if status == ProjectStatus.PUBLISHED:
        raise InvalidStatusError(
            "published status is only allowed via publish endpoint"
        )
