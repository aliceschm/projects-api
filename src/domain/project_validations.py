from datetime import datetime
from sqlalchemy.orm import Session
from src import models
from src.domain.exceptions import InvalidDeployDateError, InvalidStatusError, SlugAlreadyExistsError


def validate_deploy_date(deploy_date):
    if deploy_date and deploy_date > datetime.date(datetime.now()):
        raise InvalidDeployDateError()


def validate_slug_unique(db: Session, slug: str):
    slug_exists = db.query(models.Projects).filter(models.Projects.slug == slug).first()
    if slug_exists:
        raise SlugAlreadyExistsError()


def validate_status(status, allowed):
    if status not in allowed:
        raise InvalidStatusError()
