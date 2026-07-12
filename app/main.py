from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .routers import admin, auth, lists, todos, users, views

openapi_tags = [
    {"name": "Auth", "description": "User registration and login (JWT issuance)."},
    {"name": "Todos", "description": "Manage the authenticated user's own todos."},
    {"name": "Lists", "description": "Manage the authenticated user's own lists of todos."},
    {"name": "Admin", "description": "Admin-only endpoints spanning every user's todos."},
    {"name": "Users", "description": "Manage the authenticated user's own profile."},
    {"name": "Dashboard", "description": "Server-rendered HTML pages."},
]

app = FastAPI(
    title="Google Tasks API",
    description="A FastAPI backend inspired by Google Tasks, featuring lists, tasks, "
    "due dates, priorities, labels, authentication, and RESTful APIs.",
    version="0.2.0",
    openapi_tags=openapi_tags,
)

app.include_router(views.router)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(lists.router)
app.include_router(admin.router)
app.include_router(users.router)
