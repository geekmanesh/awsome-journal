from database import base
from sqlalchemy import Column, Integer


class Todos(base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
