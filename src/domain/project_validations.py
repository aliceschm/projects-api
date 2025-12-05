from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src import models

def validate_deploy_date(deploy_date):
    if deploy_date and deploy_date > datetime.date(datetime.now()):
        raise HTTPException(
            status_code=400,
            detail="Deploy date cannot be in the future"
        )

def validate_slug_unique(db: Session, slug: str):
    slug_exists = db.query(models.Projects).filter(models.Projects.slug == slug).first()
    if slug_exists:
        raise HTTPException(status_code=400, detail="Slug already exists")

def validate_status(status, allowed):
    if status not in allowed:
        raise HTTPException(status_code=400, detail="Invalid status")
