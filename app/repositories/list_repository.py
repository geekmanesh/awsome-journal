import uuid

from sqlalchemy.orm import Session

from app.models.list import List


def create_default(db: Session, owner_id: uuid.UUID) -> List:
    default_list = List(
        title="Tasks",
        description="Your default task list.",
        priority=1,
        owner_id=owner_id,
    )
    db.add(default_list)
    db.commit()
    db.refresh(default_list)
    return default_list
