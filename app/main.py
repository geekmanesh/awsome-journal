from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .routers import admin, auth, lists, todos, users, views

app = FastAPI()

templates = Jinja2Templates(directory="app/templates/")

app.mount("/static", StaticFiles(directory="app/static/"), name="static")


app.include_router(views.router)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(lists.router)
app.include_router(admin.router)
app.include_router(users.router)
