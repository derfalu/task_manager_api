from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "task_manager",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["app.services.task_scheduler"],
)

celery_app.conf.task_routes = {
    "app.services.task_scheduler.*": {"queue": "celery"},
}

celery_app.conf.beat_schedule = {
    "check-overdue-every-minute": {
        "task": "app.services.task_scheduler.check_overdue_tasks",
        "schedule": crontab(minute="*"),
    },
}

celery_app.conf.timezone = "UTC"
