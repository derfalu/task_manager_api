from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.services.user_service import get_user_by_username
from app.models.user import User
from app.core.security import verify_token
from app.core.exceptions import credentials_exception, user_not_found_exception

# Зависимость FastAPI для получения Bearer-токена из заголовков Authorization
http_bearer = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: Session = Depends(get_db),
) -> User:
    """
    Извлекает текущего пользователя из JWT-токена.

    - Проверяет валидность токена
    - Получает имя пользователя из payload
    - Загружает пользователя из базы данных

    :raises credentials_exception: если токен недействителен или отсутствует "sub"
    :raises user_not_found_exception: если пользователь не найден в БД
    :return: Объект User
    """
    token = credentials.credentials

    payload = verify_token(token)
    if not payload or "sub" not in payload:
        raise credentials_exception()

    username = payload["sub"]
    user = get_user_by_username(db, username)
    if user is None:
        raise user_not_found_exception()
    return user
