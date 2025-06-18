from app.core.celery.celery_worker import celery_app
from app.db.database import SessionLocal
from app.models.task import Task, StatusEnum
from datetime import datetime, timezone
import logging
from sqlalchemy import or_


@celery_app.task
def check_overdue_tasks():
    db = SessionLocal()
    now = datetime.now(timezone.utc)
    logging.warning(f"[DEBUG] Текущее время: {now}")

    tasks = (
        db.query(Task)
        .filter(Task.due_date != None)
        .filter(Task.due_date < now)
        .filter(Task.status != StatusEnum.done)
        .filter(or_(Task.is_overdue == False, Task.is_overdue == None))  # ✅ критично!
        .all()
    )

    logging.warning(f"[DEBUG] Найдено задач: {len(tasks)}")

    for task in tasks:
        task.is_overdue = True
        logging.warning(f"[OVERDUE] Task {task.id} — {task.title} просрочена")

    db.commit()
    db.close()
