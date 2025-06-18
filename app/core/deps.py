from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.services.user_service import get_user_by_username
from app.models.user import User
from app.core.security import verify_token
from jose import JWTError

http_bearer = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials

    payload = verify_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось подтвердить учетные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = payload["sub"]
    user = get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user
