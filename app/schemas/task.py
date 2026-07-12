import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.repeat import RepeatRequest, RepeatResponse


class TaskRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=1000)
    priority: int = Field(gt=0, lt=6)
    complete: bool
    list_id: int
    repeat: RepeatRequest | None = Field(
        default=None, description="Omit for a one-off task; provide to make it recur."
    )


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    priority: int
    complete: bool
    owner_id: uuid.UUID
    list_id: int
    repeat: RepeatResponse | None = None
