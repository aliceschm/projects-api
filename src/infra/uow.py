from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.domain.exceptions import SlugAlreadyExistsError
from src.infra.repositories.projects import ProjectsRepository


class UnitOfWork:
    """
    One UnitOfWork per request.
    Holds the DB session + repositories and controls commit/rollback.
    """

    def __init__(self, db: Session):
        self.db = db
        self.projects = ProjectsRepository(db)

    def rollback(self) -> None:
        self.db.rollback()

    def refresh(self, instance) -> None:
        self.db.refresh(instance)

    def commit(self) -> None:
        try:
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            if "projects_slug_key" in str(e.orig):
                raise SlugAlreadyExistsError()
            raise
