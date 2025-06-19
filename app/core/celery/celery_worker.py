from celery import Celery
from celery.schedules import crontab
from app.core import settings

# Инициализация Celery-приложения
celery_app = Celery(
    "task_manager",  # Название приложения
    broker=settings.celery_broker_url,  # URL брокера сообщений(Redis)
    backend=settings.celery_result_backend,  # URL backend-а для хранения результатов
    include=["app.services.task_scheduler"],  # Задачи, которые Celery должен видеть
)

# Роутинг задач — все задачи из task_scheduler пойдут в очередь "celery"
celery_app.conf.task_routes = {
    "app.services.task_scheduler.*": {"queue": "celery"},
}

# Планировщик Beat — запуск задачи по расписанию
celery_app.conf.beat_schedule = {
    "check-overdue-every-minute": {
        "task": "app.services.task_scheduler.check_overdue_tasks",
        "schedule": crontab(minute="*"),  # Каждую минуту
    },
}

# Установка временной зоны
celery_app.conf.timezone = settings.celery_timezone
