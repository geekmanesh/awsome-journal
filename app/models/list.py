from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base

class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    todos = relationship(
        "Todos",
        back_populates="list",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
