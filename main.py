from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from models import Todos
from database import engine, session_local

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    sqlite_db = session_local()

    try:
        yield sqlite_db
    finally:
        sqlite_db.close()


sqlite_db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
async def read_all_todos(db: sqlite_db_dependency):
    return db.query(Todos).all()
