from fastapi import FastAPI

from .routers import admin, auth, lists, tasks, users

openapi_tags = [
    {"name": "Auth", "description": "User registration and login (JWT issuance)."},
    {"name": "Tasks", "description": "Manage the authenticated user's own tasks."},
    {"name": "Lists", "description": "Manage the authenticated user's own lists of tasks."},
    {"name": "Admin", "description": "Admin-only endpoints spanning every user's tasks."},
    {"name": "Users", "description": "Manage the authenticated user's own profile."},
]

app = FastAPI(
    title="Google Tasks API",
    description="A FastAPI backend inspired by Google Tasks, featuring lists, tasks, "
    "due dates, priorities, labels, authentication, and RESTful APIs.",
    version="0.2.0",
    openapi_tags=openapi_tags,
)

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(lists.router)
app.include_router(admin.router)
app.include_router(users.router)
