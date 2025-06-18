from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.schemas.tag import TagRead
import enum


class StatusEnum(str, enum.Enum):
    new = "new"
    in_progress = "in_progress"
    done = "done"


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: StatusEnum = StatusEnum.new
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = Field(default_factory=list)


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None


class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: StatusEnum
    due_date: Optional[datetime]
    created_at: datetime
    tags: List[TagRead] = []
    is_overdue: bool

    model_config = {"from_attributes": True}
