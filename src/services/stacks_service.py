# Services that will alter stacks table in the db
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

def update_project_stacks(db, project_id: int, stack_names: list[str]):

    cleaned_names = {name.strip() for name in stack_names if name and name.strip()}
    cleaned_names = list(cleaned_names)

    # Stacks atuais
    existing = (
        db.query(models.ProjectStack.stack_id)
          .filter(models.ProjectStack.project_id == project_id)
          .all()
    )
    existing_ids = {row.stack_id for row in existing}

    # Garantir existência das stacks (criar se não existir)
    new_stack_objs = []
    for name in cleaned_names:
        stack_obj = get_or_create_stack(db, name)
        new_stack_objs.append(stack_obj)

    new_ids = {s.id for s in new_stack_objs}

    # Calcular delta
    to_add = new_ids - existing_ids
    to_remove = existing_ids - new_ids

    # Inserir
    for stack_id in to_add:
        db.add(models.ProjectStack(project_id=project_id, stack_id=stack_id))

    # Remover
    if to_remove:
        db.query(models.ProjectStack).filter(
            models.ProjectStack.project_id == project_id,
            models.ProjectStack.stack_id.in_(to_remove)
        ).delete(synchronize_session=False)

    db.flush()
