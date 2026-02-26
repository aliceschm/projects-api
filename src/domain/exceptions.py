# Raise domain validations exceptions


class DomainError(Exception):
    """Base class for domain exceptions."""

    default_message = "Domain error"

    def __init__(self, message: str | None = None):
        # Store final message explicitly for consistency and extensibility
        self.message = message or self.default_message

        # Initialize base Exception with the resolved message
        super().__init__(self.message)

    def __str__(self) -> str:
        # Ensure string representation always returns the stored message
        return self.message


class InvalidDeployDateError(DomainError):
    """Raised when a deploy date in the future is provided for a project."""

    default_message = "Deploy date cannot be in the future"


class InvalidStatusError(DomainError):
    """Raised when an invalid status (not in ProjectStatus Enum) is provided for a project."""

    default_message = "Invalid status"


class ProjectNotFoundError(DomainError):
    """Raised when a project with the specified ID does not exist."""

    default_message = "Project not found"


class ProjectNotPublishableError(DomainError):
    """Raised when trying to publish a project that doesn't meet publishable criteria."""

    default_message = "Project cannot be published due to missing required data"


class EmptyPatchError(DomainError):
    """Raised when a PATCH request is made without any fields to update."""

    default_message = "Please enter a value to be updated"


class ProjectDeleteNotAllowedError(DomainError):
    """Raised when a published project is attempted to be deleted."""

    default_message = "Published projects cannot be deleted"


class UniqueConstraintError(DomainError):
    """Raised when a unique constraint is violated in the database."""
    default_message = "Unique constraint violated"

    def __init__(self, message: str | None = None, *, constraint: str | None = None):
        self.constraint = constraint

        # Build a richer message when constraint is available
        if message is None and constraint:
            message = f"{self.default_message}: {constraint}"

        super().__init__(message)
