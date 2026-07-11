from fastapi import APIRouter, Request
from app.core.settings import templates

router = APIRouter(tags=["Dashboard"], prefix="/dashboard")


@router.get(
    "/login",
    summary="Login page",
    description="Renders the server-side login form.",
)
async def login_page(request: Request):
    return templates.TemplateResponse(
        name="login.html", context={"request": request}, request=request
    )


@router.get(
    "/register",
    summary="Registration page",
    description="Renders the server-side registration form.",
)
async def register_page(request: Request):
    return templates.TemplateResponse(
        request,
        "register.html",
        {"request": request},
    )
