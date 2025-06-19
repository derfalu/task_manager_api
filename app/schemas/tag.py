from pydantic import BaseModel


class TagBase(BaseModel):
    """
    Базовая схема тега (используется для наследования).

    Поля:
    - name: название тега
    """

    name: str


class TagCreate(TagBase):
    """
    Схема для создания нового тега.

    Наследует только поле `name`.
    """

    pass


class TagRead(TagBase):
    """
    Схема для чтения информации о теге.

    Дополнительно включает:
    - id: уникальный идентификатор тега
    """

    id: int

    model_config = {
        "from_attributes": True
    }  # Позволяет автоматически преобразовывать ORM-модель в Pydantic-схему
