from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.core.database import Base, engine
from .routers import admin, auth, todos, users

app = FastAPI()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="app/templates/")

app.mount("/static", StaticFiles(directory="app/static/"), name="static")


@app.get("/")
def test(request: Request):
    return templates.TemplateResponse(name="home.html", request=request)


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
