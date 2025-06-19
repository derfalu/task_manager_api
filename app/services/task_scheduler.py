from app.core.celery.celery_worker import celery_app
from app.db.database import SessionLocal
from app.models.task import Task, StatusEnum
from datetime import datetime, timezone
import logging
from sqlalchemy import or_

logger = logging.getLogger(__name__)


@celery_app.task
def check_overdue_tasks():
    """
    Фоновая Celery-задача для проверки просроченных задач.

    Задачи считаются просроченными, если:
    - Установлен срок выполнения (`due_date`)
    - `due_date` раньше текущего времени
    - Статус не `done`
    - Поле `is_overdue` ещё не установлено

    Такие задачи помечаются как просроченные (`is_overdue = True`) и логируются.
    """
    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        logger.info(f"[DEBUG] Текущее время: {now}")

        tasks = (
            db.query(Task)
            .filter(Task.due_date.isnot(None))
            .filter(Task.due_date < now)
            .filter(Task.status != StatusEnum.done)
            .filter(or_(Task.is_overdue == False, Task.is_overdue == None))
            .all()
        )

        logger.info(f"[DEBUG] Найдено просроченных задач: {len(tasks)}")

        for task in tasks:
            task.is_overdue = True
            logger.warning(f"[OVERDUE] Задача {task.id} — '{task.title}' просрочена")

        db.commit()
    except Exception as e:
        logger.exception(f"[ERROR] Ошибка при проверке просроченных задач: {e}")
    finally:
        db.close()
