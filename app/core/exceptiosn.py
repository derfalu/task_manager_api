from fastapi import  status, HTTPException


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


def conflict_exception(detail: str = "Конфликт данных"):
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=detail,
    )
