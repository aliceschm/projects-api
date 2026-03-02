# Raise domain validations exceptions
class DomainError(Exception):
    """Base class for domain exceptions."""

    default_message = "Domain error"
    status_code = 400
    code = "domain_error"

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message


class InvalidDeployDateError(DomainError):
    """Raised when a deploy date in the future is provided for a project."""

    default_message = "Deploy date cannot be in the future"
    status_code = 422
    code = "invalid_deploy_date"


class InvalidStatusError(DomainError):
    """Raised when an invalid status (not in ProjectStatus Enum) is provided for a project."""

    default_message = "Invalid status"
    status_code = 422
    code = "invalid_status"


class ProjectNotFoundError(DomainError):
    """Raised when a project with the specified ID does not exist."""

    default_message = "Project not found"
    status_code = 404
    code = "project_not_found"


class ProjectNotPublishableError(DomainError):
    """Raised when trying to publish a project that doesn't meet publishable criteria."""

    default_message = "Project cannot be published due to missing required data"
    status_code = 409
    code = "project_not_publishable"


class EmptyPatchError(DomainError):
    """Raised when a PATCH request is made without any fields to update."""

    default_message = "Please enter a value to be updated"
    status_code = 422
    code = "empty_patch"


class ActionNotAllowedError(DomainError):
    """Raised when a published project is attempted to be edited or deleted."""

    default_message = "Published projects cannot be edited or deleted"
    status_code = 409
    code = "action_not_allowed"


class SlugAlreadyExistsError(DomainError):
    """Raised when a project with the same slug already exists."""

    default_message = "Slug already exists"
    status_code = 409
    code = "slug_already_exists"


class ProjectDescriptionNotFoundError(DomainError):
    """Raised when a project description in the requested language is not found."""

    default_message = "Project description not found for the specified language"
    status_code = 404
    code = "project_description_not_found"
