from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserRead, Token, UserLogin
from app.services.user_service import create_user, authenticate_user
from app.core.security import create_access_token
from app.db.deps import get_db
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Пользователь 👤"])


@router.post(
    "/register",
    response_model=UserRead,
    summary="Регистрация пользователя",
    description="""
Регистрирует нового пользователя в системе.

- Требует уникальные `username` и `email`
- Возвращает данные созданного пользователя
""",
)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.post(
    "/login",
    response_model=Token,
    summary="Аутентификация пользователя",
    description="""
Аутентифицирует пользователя по имени и паролю.

- Возвращает JWT-токен при успешной аутентификации
- В случае ошибки — 401 Unauthorized
""",
)
def login(user: UserLogin, db: Session = Depends(get_db)):
    user_in_db = authenticate_user(db, user.username, user.password)
    if not user_in_db:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    token = create_access_token({"sub": user_in_db.username})
    return {"access_token": token, "token_type": "bearer"}


@router.get(
    "/profile",
    response_model=UserRead,
    summary="Получить текущего пользователя",
    description="""
Возвращает данные текущего авторизованного пользователя.

- Требуется авторизация через Bearer-токен
""",
)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
