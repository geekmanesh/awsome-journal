from fastapi import APIRouter, HTTPException, Path
from starlette import status

from app.dependencies import db_dependency, user_dependency
from app.models.todo import Todos
from app.schemas.todo import TodoResponse

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


def _require_admin(user: dict) -> None:
    if user.get("user_role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges are required for this action.",
        )


@router.get(
    "/todos",
    status_code=status.HTTP_200_OK,
    response_model=list[TodoResponse],
    summary="List every user's todos",
    description="Admin-only. Returns all todos across all users.",
)
async def read_all_todos(user: user_dependency, db: db_dependency):
    _require_admin(user)

    return db.query(Todos).all()


@router.get(
    "/todos/{todo_id}",
    status_code=status.HTTP_200_OK,
    response_model=TodoResponse,
    summary="Get any user's todo by ID",
    description="Admin-only. Returns a single todo regardless of its owner.",
)
async def read_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    _require_admin(user)

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No todo found with this id!",
        )
    return todo_model


@router.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete any user's todo",
    description="Admin-only. Permanently deletes a todo regardless of its owner.",
)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    _require_admin(user)

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found!"
        )

    db.delete(todo_model)
    db.commit()
