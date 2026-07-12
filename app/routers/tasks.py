from fastapi import APIRouter, HTTPException, Path
from starlette import status

from app.dependencies import db_dependency, user_dependency
from app.models.list import List
from app.models.repeat import Repeat
from app.models.task import Task
from app.schemas.task import TaskRequest, TaskResponse

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[TaskResponse],
    summary="List your tasks",
    description="Returns every task owned by the authenticated user.",
)
async def read_all_tasks(user: user_dependency, db: db_dependency):
    return db.query(Task).filter(Task.owner_id == user.get("id")).all()


@router.get(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=TaskResponse,
    summary="Get a task by ID",
    description="Returns a single task owned by the authenticated user.",
)
async def read_task(
    user: user_dependency, db: db_dependency, task_id: int = Path(gt=0)
):
    task_model = (
        db.query(Task)
        .filter(Task.id == task_id)
        .filter(Task.owner_id == user.get("id"))
        .first()
    )
    if task_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No task found with this id!",
        )
    return task_model


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskResponse,
    summary="Create a task",
    description="Creates a new task in one of the authenticated user's own lists. "
    "`list_id` must reference a list owned by the caller.",
)
async def create_task(
    user: user_dependency,
    db: db_dependency,
    task_request: TaskRequest,
):
    list_model = (
        db.query(List)
        .filter(List.id == task_request.list_id)
        .filter(List.owner_id == user.get("id"))
        .first()
    )
    if list_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="List not found!"
        )

    task_model = Task(
        **task_request.model_dump(exclude={"repeat"}),
        owner_id=user.get("id"),
    )

    if task_request.repeat is not None:
        task_model.repeat = Repeat(**task_request.repeat.model_dump())

    db.add(task_model)
    db.commit()
    db.refresh(task_model)

    return task_model


@router.put(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update a task",
    description="Replaces the fields of a task owned by the authenticated user. "
    "`list_id` must reference a list owned by the caller.",
)
async def update_task(
    user: user_dependency,
    db: db_dependency,
    task_request: TaskRequest,
    task_id: int = Path(gt=0),
):
    task_model = (
        db.query(Task)
        .filter(Task.id == task_id)
        .filter(Task.owner_id == user.get("id"))
        .first()
    )
    if task_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found!"
        )

    list_model = (
        db.query(List)
        .filter(List.id == task_request.list_id)
        .filter(List.owner_id == user.get("id"))
        .first()
    )
    if list_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="List not found!"
        )

    task_model.title = task_request.title
    task_model.description = task_request.description
    task_model.priority = task_request.priority
    task_model.complete = task_request.complete
    task_model.list_id = task_request.list_id

    if task_request.repeat is None:
        if task_model.repeat is not None:
            db.delete(task_model.repeat)
    elif task_model.repeat is None:
        task_model.repeat = Repeat(**task_request.repeat.model_dump())
    else:
        for field, value in task_request.repeat.model_dump().items():
            setattr(task_model.repeat, field, value)

    db.add(task_model)
    db.commit()


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Permanently deletes a task owned by the authenticated user.",
)
async def delete_task(
    user: user_dependency, db: db_dependency, task_id: int = Path(gt=0)
):
    task_model = (
        db.query(Task)
        .filter(Task.id == task_id)
        .filter(Task.owner_id == user.get("id"))
        .first()
    )
    if task_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found!"
        )

    db.delete(task_model)
    db.commit()
