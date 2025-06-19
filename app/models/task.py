from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
import enum
from app.models.tag import task_tags


class StatusEnum(str, enum.Enum):
    """
    Перечисление возможных статусов задачи.
    """

    new = "new"
    in_progress = "in_progress"
    done = "done"


class Task(Base):
    """
    Модель задачи, связанной с пользователем и тегами.

    Атрибуты:
    - title: название задачи (обязательное)
    - description: описание задачи
    - status: текущий статус (enum)
    - due_date: срок выполнения
    - created_at: дата создания
    - is_overdue: логический флаг просроченности
    - user_id: внешний ключ на владельца задачи
    - tags: многие-ко-многим связь с тегами
    """

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum(StatusEnum), default=StatusEnum.new)
    due_date = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_overdue = Column(Boolean, default=False)

    # Связь многие-ко-многим с тегами через промежуточную таблицу task_tags
    tags = relationship("Tag", secondary=task_tags, backref="tasks")
