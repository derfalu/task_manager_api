from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


# Ассоциативная таблица для связи многие-ко-многим между задачами и тегами
task_tags = Table(
    "task_tags",
    Base.metadata,
    Column("task_id", ForeignKey("tasks.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Tag(Base):
    """
    Модель тега, принадлежащего пользователю.

    Каждый тег:
    - имеет уникальное имя в рамках одного пользователя
    - может быть связан с несколькими задачами
    """

    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Связь с пользователем (владелец тега)
    user = relationship("User", backref="tags")

from app.models.user import User
