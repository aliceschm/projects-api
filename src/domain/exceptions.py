# Raise domain validations exceptions

class DomainError(Exception):
    """Base class for domain exceptions"""
    pass

class InvalidDeployDateError(DomainError):
    pass

class SlugAlreadyExistsError(DomainError):
    pass

class InvalidStatusError(DomainError):
    pass

class ProjectNotFoundError(DomainError):
    pass