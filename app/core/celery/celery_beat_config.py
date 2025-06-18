from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    "check-overdue-every-minute": {
        "task": "app.services.task_scheduler.check_overdue_tasks",
        "schedule": crontab(minute="*"),
    },
}
