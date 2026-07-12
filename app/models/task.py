from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    list_id = Column(Integer, ForeignKey("lists.id", ondelete="CASCADE"), nullable=False)

    list = relationship("List", back_populates="tasks")
    repeat = relationship(
        "Repeat",
        back_populates="task",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
