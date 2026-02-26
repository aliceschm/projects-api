from fastapi import Depends
from sqlalchemy.orm import Session

from src.infra.db.database import get_db
from src.infra.repositories.projects import UnitOfWork


def get_uow(db: Session = Depends(get_db)) -> UnitOfWork:
    return UnitOfWork(db)
