from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.tag import TagRead, TagCreate
from app.services import tag_service
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/tags", tags=["Теги 📌"])


@router.get(
    "/",
    response_model=list[TagRead],
    summary="Получить список тегов",
    description="Возвращает все теги текущего пользователя",
)
def list_tags(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return tag_service.get_all_tags(db, user)


@router.post(
    "/",
    response_model=TagRead,
    status_code=201,
    summary="Создать новый тег",
    description="""
Создаёт новый тег с указанным названием.

- Название должно быть уникальным для текущего пользователя.
""",
)
def create_tag(
    tag_in: TagCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return tag_service.create_tag(db, tag_in, user)


@router.delete(
    "/{tag_id}",
    status_code=204,
    summary="Удалить тег",
    description="""
Удаляет тег по ID, если он принадлежит текущему пользователю.

⚠️ Если тег связан с задачами, произойдёт ошибка.
""",
)
def delete_tag(
    tag_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    tag_service.delete_tag(db, tag_id, user)
