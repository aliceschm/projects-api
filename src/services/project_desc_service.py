# Services related to projectdesc table
from sqlalchemy.orm import Session
from src import models


def update_project_desc(db, project_id: int, desc_patches: list):
    for desc_patch in desc_patches:
        data = desc_patch.model_dump(exclude_unset=True)
        lang = desc_patch.lang

        # Search project
        desc = (
            db.query(models.ProjectDesc)
            .filter(
                models.ProjectDesc.id == project_id, models.ProjectDesc.lang == lang
            )
            .first()
        )

        # Verify empty fields
        is_empty = all(
            data.get(field) in (None, "")
            for field in ("name", "about", "full_desc")
            if field in data
        )

        if is_empty:
            if desc:
                db.delete(desc)
            continue

        # Create if it doesn't exist
        if not desc:
            desc = models.ProjectDesc(id=project_id, lang=lang)
            db.add(desc)

        # Update only non empty fields
        for field in ("name", "about", "full_desc"):
            if field in data:
                setattr(desc, field, data[field])

    db.flush()
