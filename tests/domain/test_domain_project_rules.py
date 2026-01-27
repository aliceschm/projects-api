import pytest
from datetime import date
from src.domain.project_rules import (
    validate_project_publishable,
    validate_status_not_published,
    validate_status,
)
from src.domain.exceptions import (
    ProjectNotPublishableError,
    InvalidStatusError,
)
from src.schemas import ProjectLang, ProjectStatus
from tests.domain.fakes import FakeProject, FakeDescription


def test_published_status_is_not_allowed_directly():
    with pytest.raises(InvalidStatusError):
        validate_status_not_published(ProjectStatus.PUBLISHED)


def test_non_published_status_is_allowed():
    validate_status_not_published(ProjectStatus.DRAFT)


def test_project_without_deploy_date_is_not_publishable():
    project = FakeProject(stacks=["FastAPI"], descriptions=[])
    with pytest.raises(ProjectNotPublishableError):
        validate_project_publishable(project)


def test_project_missing_required_languages_is_not_publishable():
    descriptions = [
        FakeDescription(
            lang=ProjectLang.PT.value,
            name="Projeto",
            about="Sobre",
            full_desc="Descrição",
        )
    ]

    project = FakeProject(
        deploy_date=date.today(), stacks=["FastAPI"], descriptions=descriptions
    )

    with pytest.raises(ProjectNotPublishableError):
        validate_project_publishable(project)


def test_project_with_incomplete_description_is_not_publishable():
    descriptions = [
        FakeDescription(
            lang=ProjectLang.PT.value,
            name="Projeto",
            about=None,  # missing field
            full_desc="Descrição",
        ),
        FakeDescription(
            lang=ProjectLang.EN.value,
            name="Project",
            about="About",
            full_desc="Description",
        ),
    ]

    project = FakeProject(
        deploy_date=date.today(), stacks=["FastAPI"], descriptions=descriptions
    )

    with pytest.raises(ProjectNotPublishableError):
        validate_project_publishable(project)


def test_valid_project_is_publishable():
    descriptions = [
        FakeDescription(
            lang=ProjectLang.PT.value,
            name="Projeto",
            about="Sobre",
            full_desc="Descrição",
        ),
        FakeDescription(
            lang=ProjectLang.EN.value,
            name="Project",
            about="About",
            full_desc="Description",
        ),
    ]

    project = FakeProject(
        deploy_date=date.today(), stacks=["FastAPI"], descriptions=descriptions
    )

    validate_project_publishable(project)


def test_validate_status_not_allowed():
    allowed = {ProjectStatus.DRAFT}

    with pytest.raises(InvalidStatusError):
        validate_status(ProjectStatus.ARCHIVED, allowed)


def test_validate_status_allowed():
    allowed = {ProjectStatus.DRAFT, ProjectStatus.ARCHIVED}

    validate_status(ProjectStatus.DRAFT, allowed)
