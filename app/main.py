from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

from app.api import user, task, tag
from app.core.exceptions import (
    validation_exception_handler,
    integrity_exception_handler,
    unhandled_exception_handler,
)

# Инициализация FastAPI-приложения
app = FastAPI(
    title="Task Manager API",
    description="Простое REST API для управления задачами с поддержкой тегов и JWT-аутентификации.",
    version="1.0.0",
)

# Подключение роутеров
app.include_router(user.router)  # Роуты пользователей
app.include_router(tag.router)  # Роуты тегов
app.include_router(task.router)  # Роуты задач

# Обработчики ошибок
app.add_exception_handler(
    RequestValidationError, validation_exception_handler
)  # 422 ошибки валидации
app.add_exception_handler(
    IntegrityError, integrity_exception_handler
)  # 400 ошибки целостности БД
app.add_exception_handler(
    Exception, unhandled_exception_handler
)  # 500 внутренние ошибки
