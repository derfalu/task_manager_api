from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    """
    Схема для регистрации нового пользователя.

    Поля:
    - username: имя пользователя
    - email: email (валидируется как EmailStr)
    - password: пароль в открытом виде
    """

    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    """
    Схема для отображения информации о пользователе.

    Поля:
    - id: уникальный идентификатор
    - username: имя пользователя
    - email: email
    """

    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)  # Преобразование из ORM-модели


class UserLogin(BaseModel):
    """
    Схема для входа пользователя.

    Поля:
    - username: имя пользователя
    - password: пароль
    """

    username: str
    password: str


class Token(BaseModel):
    """
    Схема токена, возвращаемого после авторизации.

    Поля:
    - access_token: JWT-токен доступа
    - token_type: тип токена (по умолчанию 'bearer')
    """

    access_token: str
    token_type: str = "bearer"
