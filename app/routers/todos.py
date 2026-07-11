from fastapi import APIRouter, HTTPException, Path
from starlette import status

from app.dependencies import db_dependency, user_dependency
from app.models.list import List
from app.models.todo import Todos
from app.schemas.todo import TodoRequest, TodoResponse

router = APIRouter(
    prefix="/todos",
    tags=["Todos"],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[TodoResponse],
    summary="List your todos",
    description="Returns every todo owned by the authenticated user.",
)
async def read_all_todos(user: user_dependency, db: db_dependency):
    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()


@router.get(
    "/{todo_id}",
    status_code=status.HTTP_200_OK,
    response_model=TodoResponse,
    summary="Get a todo by ID",
    description="Returns a single todo owned by the authenticated user.",
)
async def read_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No todo found with this id!",
        )
    return todo_model


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=TodoResponse,
    summary="Create a todo",
    description="Creates a new todo in one of the authenticated user's own lists. "
    "`list_id` must reference a list owned by the caller.",
)
async def create_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest,
):
    list_model = (
        db.query(List)
        .filter(List.id == todo_request.list_id)
        .filter(List.owner_id == user.get("id"))
        .first()
    )
    if list_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="List not found!"
        )

    todo_model = Todos(
        **todo_request.model_dump(),
        owner_id=user.get("id"),
    )

    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)

    return todo_model


@router.put(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update a todo",
    description="Replaces the fields of a todo owned by the authenticated user. "
    "`list_id` must reference a list owned by the caller.",
)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0),
):
    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found!"
        )

    list_model = (
        db.query(List)
        .filter(List.id == todo_request.list_id)
        .filter(List.owner_id == user.get("id"))
        .first()
    )
    if list_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="List not found!"
        )

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    todo_model.list_id = todo_request.list_id

    db.add(todo_model)
    db.commit()


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a todo",
    description="Permanently deletes a todo owned by the authenticated user.",
)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found!"
        )

    db.delete(todo_model)
    db.commit()
