# Raise domain validations exceptions


class DomainError(Exception):
    """Base class for domain exceptions"""

    default_message = "Domain error"

    def __init__(self, message: str | None = None):
        # Initialize base Exception with provided message or class default
        super().__init__(message or self.default_message)


class InvalidDeployDateError(DomainError):
    default_message = "Deploy date cannot be in the future"


class SlugAlreadyExistsError(DomainError):
    default_message = "Slug already exists"


class InvalidStatusError(DomainError):
    default_message = "Invalid status"


class ProjectNotFoundError(DomainError):
    default_message = "Project not found"


class ProjectNotPublishableError(DomainError):
    default_message = "Project cannot be published due to missing required data"


class EmptyPatchError(DomainError):
    default_message = "Please enter a value to be updated"


class ProjectDeleteNotAllowedError(DomainError):
    default_message = "Published projects cannot be deleted"
