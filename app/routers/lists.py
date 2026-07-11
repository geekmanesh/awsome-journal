from fastapi import APIRouter, HTTPException, Path
from starlette import status

from app.dependencies import db_dependency, user_dependency
from app.models.list import List
from app.schemas.list import ListRequest, ListResponse
from app.schemas.todo import TodoResponse

router = APIRouter(
    prefix="/lists",
    tags=["Lists"],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[ListResponse],
    summary="List your lists",
    description="Returns every list owned by the authenticated user.",
)
async def read_all_lists(user: user_dependency, db: db_dependency):
    return db.query(List).filter(List.owner_id == user.get("id")).all()


@router.get(
    "/{list_id}",
    status_code=status.HTTP_200_OK,
    response_model=ListResponse,
    summary="Get a list by ID",
    description="Returns a single list owned by the authenticated user.",
)
async def read_list(
    user: user_dependency, db: db_dependency, list_id: int = Path(gt=0)
):
    list_model = (
        db.query(List)
        .filter(List.id == list_id)
        .filter(List.owner_id == user.get("id"))
        .first()
    )
    if list_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No list found with this id!",
        )
    return list_model


@router.get(
    "/{list_id}/todos",
    status_code=status.HTTP_200_OK,
    response_model=list[TodoResponse],
    summary="List the todos in a list",
    description="Returns every todo belonging to a list owned by the authenticated user.",
)
async def read_list_todos(
    user: user_dependency, db: db_dependency, list_id: int = Path(gt=0)
):
    list_model = (
        db.query(List)
        .filter(List.id == list_id)
        .filter(List.owner_id == user.get("id"))
        .first()
    )
    if list_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No list found with this id!",
        )
    return list_model.todos


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ListResponse,
    summary="Create a list",
    description="Creates a new list owned by the authenticated user.",
)
async def create_list(
    user: user_dependency,
    db: db_dependency,
    list_request: ListRequest,
):
    list_model = List(
        **list_request.model_dump(),
        owner_id=user.get("id"),
    )

    db.add(list_model)
    db.commit()
    db.refresh(list_model)

    return list_model


@router.put(
    "/{list_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update a list",
    description="Replaces the fields of a list owned by the authenticated user.",
)
async def update_list(
    user: user_dependency,
    db: db_dependency,
    list_request: ListRequest,
    list_id: int = Path(gt=0),
):
    list_model = (
        db.query(List)
        .filter(List.id == list_id)
        .filter(List.owner_id == user.get("id"))
        .first()
    )
    if list_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="List not found!"
        )

    list_model.title = list_request.title
    list_model.description = list_request.description
    list_model.priority = list_request.priority

    db.add(list_model)
    db.commit()


@router.delete(
    "/{list_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a list",
    description="Permanently deletes a list owned by the authenticated user, "
    "along with all of its todos.",
)
async def delete_list(
    user: user_dependency, db: db_dependency, list_id: int = Path(gt=0)
):
    list_model = (
        db.query(List)
        .filter(List.id == list_id)
        .filter(List.owner_id == user.get("id"))
        .first()
    )

    if list_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="List not found!"
        )

    db.delete(list_model)
    db.commit()
