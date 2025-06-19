from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.services.user_service import get_user_by_username
from app.models.user import User
from app.core.security import verify_token
from app.core.exceptiosn import credentials_exception, user_not_found_exception

http_bearer = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials

    payload = verify_token(token)
    if not payload or "sub" not in payload:
        raise credentials_exception()

    username = payload["sub"]
    user = get_user_by_username(db, username)
    if user is None:
        raise user_not_found_exception()
    return user
