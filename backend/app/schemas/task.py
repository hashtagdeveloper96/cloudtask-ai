from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    status: TaskStatus = TaskStatus.PENDING


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    status: str | None = Field(
        default=None,
        max_length=50,
    )


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    user_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
