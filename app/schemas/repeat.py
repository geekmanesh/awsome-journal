from datetime import datetime, time

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.repeat import RepeatEndType, RepeatFrequency


class RepeatRequest(BaseModel):
    frequency: RepeatFrequency
    interval_count: int = Field(default=1, gt=0)
    time_of_day: time
    start_at: datetime
    end_type: RepeatEndType = RepeatEndType.NEVER
    end_at: datetime | None = None
    occurrences: int | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def validate_end(self):
        if self.end_type == RepeatEndType.ON_DATE and self.end_at is None:
            raise ValueError("end_at is required when end_type is 'on_date'")
        if (
            self.end_type == RepeatEndType.AFTER_OCCURRENCES
            and self.occurrences is None
        ):
            raise ValueError(
                "occurrences is required when end_type is 'after_occurrences'"
            )
        if self.end_type == RepeatEndType.NEVER and (
            self.end_at is not None or self.occurrences is not None
        ):
            raise ValueError(
                "end_at/occurrences must not be set when end_type is 'never'"
            )
        return self


class RepeatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    frequency: RepeatFrequency
    interval_count: int
    time_of_day: time
    start_at: datetime
    end_type: RepeatEndType
    end_at: datetime | None
    occurrences: int | None
