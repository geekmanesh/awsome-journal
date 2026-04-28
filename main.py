from fastapi import FastAPI, Depends, HTTPException, Path

from routers import auth, todos
from database import Base, engine
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
