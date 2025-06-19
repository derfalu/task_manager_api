from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, StatusEnum, TaskUpdate
from app.models.user import User
from app.services.tag_service import get_or_create_tags
from datetime import datetime, timezone
from app.models.tag import Tag
from typing import List, Optional
from app.core.exceptions import not_found_exception


def create_task(db: Session, user: User, task_in: TaskCreate):
    """
    Создаёт новую задачу для пользователя.
    Учитывает наличие тегов и автоматически помечает задачу как просроченную,
    если срок истёк и статус не "done".

    :param db: Сессия SQLAlchemy
    :param user: Текущий пользователь
    :param task_in: Входные данные задачи
    :return: Объект созданной задачи
    """
    tags = get_or_create_tags(db, task_in.tags, user)

    is_overdue = (
        task_in.due_date is not None
        and task_in.due_date < datetime.now(timezone.utc)
        and task_in.status != StatusEnum.done
    )

    task = Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status,
        due_date=task_in.due_date,
        user_id=user.id,
        tags=tags,
        is_overdue=is_overdue,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_user_tasks(
    db: Session,
    user: User,
    status: Optional[StatusEnum] = None,
    due_from: Optional[datetime] = None,
    due_to: Optional[datetime] = None,
    tag_id: Optional[int] = None,
    sort_by_due_date: bool = False,
):
    """
    Получает список задач пользователя с возможностью фильтрации.

    Фильтрация по:
    - статусу
    - диапазону срока выполнения
    - тегу
    - сортировка по дате выполнения

    :return: Список задач
    """
    query = db.query(Task).filter(Task.user_id == user.id)

    if status:
        query = query.filter(Task.status == status)

    if due_from:
        query = query.filter(Task.due_date >= due_from)

    if due_to:
        query = query.filter(Task.due_date <= due_to)

    if tag_id:
        query = query.join(Task.tags).filter(Tag.id == tag_id)

    if sort_by_due_date:
        query = query.order_by(Task.due_date.asc())

    return query.all()


def get_task_by_id(db: Session, user: User, task_id: int):
    """
    Возвращает задачу по ID, если она принадлежит пользователю.

    :raises: 404, если задача не найдена
    """
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    if not task:
        raise not_found_exception("Задача")
    return task


def update_task(db: Session, user: User, task_id: int, task_in: TaskUpdate):
    """
    Обновляет задачу. Позволяет изменить:
    - заголовок
    - описание
    - статус
    - срок выполнения
    - список тегов

    :raises: 404, если задача не найдена
    :return: Обновлённый объект задачи
    """
    task = get_task_by_id(db, user, task_id)
    if not task:
        raise not_found_exception("Задача")

    for field, value in task_in.model_dump(exclude_unset=True).items():
        if field == "tags" and value is not None:
            task.tags = get_or_create_tags(db, value, user)
        else:
            setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, user: User, task_id: int):
    """
    Удаляет задачу по ID, если она принадлежит пользователю.

    :raises: 404, если задача не найдена
    """
    task = get_task_by_id(db, user, task_id)
    if not task:
        raise not_found_exception("Задача")
    db.delete(task)
    db.commit()
