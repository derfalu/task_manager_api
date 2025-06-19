from datetime import datetime, timezone, timedelta
from jose import JWTError, jwt
from app.core import settings
from passlib.context import CryptContext

# Контекст для хеширования и проверки паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Настройки JWT
SECRET_KEY = settings.jwt_secret_key
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Создаёт JWT-токен на основе переданных данных.

    :param data: Словарь с полезной нагрузкой (payload)
    :param expires_delta: Время жизни токена (если не передано — берётся из настроек)
    :return: Зашифрованный JWT-токен в виде строки
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict | None:
    """
    Проверяет и декодирует JWT-токен.

    :param token: JWT-токен в виде строки
    :return: Расшифрованный payload, либо None, если токен недействителен
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
