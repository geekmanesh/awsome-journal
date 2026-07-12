import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Time
from sqlalchemy.orm import relationship

from app.core.database import Base


class RepeatFrequency(str, enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class RepeatEndType(str, enum.Enum):
    NEVER = "never"
    ON_DATE = "on_date"
    AFTER_OCCURRENCES = "after_occurrences"


class Repeat(Base):
    __tablename__ = "repeats"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(
        Integer,
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    frequency = Column(Enum(RepeatFrequency), nullable=False)
    interval_count = Column(Integer, nullable=False, default=1)
    time_of_day = Column(Time, nullable=False)
    start_at = Column(DateTime(timezone=True), nullable=False)

    end_type = Column(
        Enum(RepeatEndType), nullable=False, default=RepeatEndType.NEVER
    )
    end_at = Column(DateTime(timezone=True), nullable=True)
    occurrences = Column(Integer, nullable=True)

    task = relationship("Task", back_populates="repeat")
