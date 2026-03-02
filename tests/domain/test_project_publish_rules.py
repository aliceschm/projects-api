import pytest
from datetime import date

from src.domain.project_rules import (
    validate_project_publishable,
    validate_status_not_published,
)
from src.domain.exceptions import (
    ProjectNotPublishableError,
    InvalidStatusError,
)
from src.domain.schemas import ProjectLang, ProjectStatus
from tests.domain.fakes import FakeProject, FakeDescription


@pytest.mark.domain
class TestStatusRules:
    """Rules that protect the publish status transition."""

    def test_published_status_is_not_allowed_directly(self):
        """Ensures projects cannot be set to PUBLISHED outside the publish flow."""
        with pytest.raises(InvalidStatusError) as exc:
            validate_status_not_published(ProjectStatus.PUBLISHED)
        assert "publish endpoint" in str(exc.value)

    def test_non_published_status_is_allowed(self):
        """Allows non-published statuses to pass validation."""
        validate_status_not_published(ProjectStatus.DRAFT)


@pytest.mark.domain
class TestPublishRules:
    """Business rules that determine if a project can be published."""

    def test_project_without_deploy_date_is_not_publishable(self):
        """Requires deploy_date before a project can be published."""
        project = FakeProject(stacks=["FastAPI"], descriptions=[])
        with pytest.raises(ProjectNotPublishableError) as exc:
            validate_project_publishable(project)
        assert "deploy_date is required" in str(exc.value)

    def test_project_without_stacks_is_not_publishable(self):
        """Requires at least one stack before publishing."""
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
            deploy_date=date.today(),
            stacks=[],
            descriptions=descriptions,
        )

        with pytest.raises(ProjectNotPublishableError) as exc:
            validate_project_publishable(project)
        assert "at least one stack is required" in str(exc.value)

    def test_project_missing_required_languages_is_not_publishable(self):
        """Requires descriptions for all supported languages."""
        descriptions = [
            FakeDescription(
                lang=ProjectLang.PT.value,
                name="Projeto",
                about="Sobre",
                full_desc="Descrição",
            )
        ]

        project = FakeProject(
            deploy_date=date.today(),
            stacks=["FastAPI"],
            descriptions=descriptions,
        )

        with pytest.raises(ProjectNotPublishableError) as exc:
            validate_project_publishable(project)
        assert "missing descriptions for languages" in str(exc.value)

    def test_project_with_incomplete_description_is_not_publishable(self):
        """Requires all mandatory description fields for each language."""
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
            deploy_date=date.today(),
            stacks=["FastAPI"],
            descriptions=descriptions,
        )

        with pytest.raises(ProjectNotPublishableError) as exc:
            validate_project_publishable(project)
        assert "description field 'about' is required" in str(exc.value)

    def test_valid_project_is_publishable(self):
        """Allows publishing when all business rules are satisfied."""
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
            deploy_date=date.today(),
            stacks=["FastAPI"],
            descriptions=descriptions,
        )

        validate_project_publishable(project)