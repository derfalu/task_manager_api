from fastapi import  status, HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
import logging

from starlette import status

logger = logging.getLogger(__name__)

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )

async def integrity_exception_handler(request: Request, exc: IntegrityError):
    logger.error(f"Integrity error: {exc}")
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Ошибка целостности данных"
        },
    )

async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500, content={"detail": "Внутренняя ошибка сервера"}
    )

def credentials_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

def user_not_found_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Пользователь по токену не найден",
    )

def not_found_exception(entity: str = "Объект"):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{entity} не найден",
    )

def already_exists_exception(entity: str = "Объект"):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"{entity} с таким именем уже существует",
    )

def existing_user_exception():
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Пользователь с таким именем/почтой уже существует",
    )

def tag_in_use_exception():
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Нельзя удалить тег, связанный с задачами",
    )
