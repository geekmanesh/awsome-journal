from fastapi import APIRouter, Request
from app.core.settings import templates

router = APIRouter(tags=["Dashboard"], prefix="/dashboard")


@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(
        name="login.html", context={"request": request}, request=request
    )
