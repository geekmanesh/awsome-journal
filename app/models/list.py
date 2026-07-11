from sqlalchemy import Column, Integer, String, ForeignKey

from app.core.database import Base

class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))
    