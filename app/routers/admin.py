from fastapi import APIRouter, HTTPException, Path
from starlette import status

from app.dependencies import db_dependency, user_dependency
from app.models.task import Task
from app.schemas.task import TaskResponse

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
    "/tasks",
    status_code=status.HTTP_200_OK,
    response_model=list[TaskResponse],
    summary="List every user's tasks",
    description="Admin-only. Returns all tasks across all users.",
)
async def read_all_tasks(user: user_dependency, db: db_dependency):
    _require_admin(user)

    return db.query(Task).all()


@router.get(
    "/tasks/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=TaskResponse,
    summary="Get any user's task by ID",
    description="Admin-only. Returns a single task regardless of its owner.",
)
async def read_task(
    user: user_dependency, db: db_dependency, task_id: int = Path(gt=0)
):
    _require_admin(user)

    task_model = db.query(Task).filter(Task.id == task_id).first()
    if task_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No task found with this id!",
        )
    return task_model


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete any user's task",
    description="Admin-only. Permanently deletes a task regardless of its owner.",
)
async def delete_task(
    user: user_dependency, db: db_dependency, task_id: int = Path(gt=0)
):
    _require_admin(user)

    task_model = db.query(Task).filter(Task.id == task_id).first()
    if task_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found!"
        )

    db.delete(task_model)
    db.commit()
