from sqlalchemy.orm import Session
from src import models

def get_or_create_stack(db: Session, stack_name: str):
    # Transform input to lowercase to compare to db lowercase column (name_normalize)
    normalized = stack_name.strip().lower()

    # Search in name_normalized column
    stack = (
        db.query(models.Stacks)
          .filter(models.Stacks.name_normalized == normalized)
          .first()
    )
    
    if stack:
        return stack

    # Inserts stack in db if not found
    new_stack = models.Stacks(
        name=stack_name.strip(),
        name_normalized=normalized
    )

    db.add(new_stack)
    db.flush()
    return new_stack
