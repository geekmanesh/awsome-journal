from fastapi import APIRouter, HTTPException, Path
from starlette import status

from app.dependencies import db_dependency, user_dependency
from app.models.list import List
from app.schemas.list import ListRequest

router = APIRouter(
    prefix="/lists",
    tags=["Lists"],
)


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_lists(user: user_dependency, db: db_dependency):
    return db.query(List).filter(List.owner_id == user.get("id")).all()


@router.get("/{list_id}", status_code=status.HTTP_200_OK)
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


@router.get("/{list_id}/todos", status_code=status.HTTP_200_OK)
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


@router.post("/", status_code=status.HTTP_201_CREATED)
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


@router.put("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
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
        raise HTTPException(status_code=404, detail="List not found!")

    list_model.title = list_request.title
    list_model.description = list_request.description
    list_model.priority = list_request.priority

    db.add(list_model)
    db.commit()


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
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
        raise HTTPException(status_code=404, detail="List not found!")

    db.delete(list_model)
    db.commit()
