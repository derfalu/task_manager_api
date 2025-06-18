from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskRead, StatusEnum, TaskUpdate
from app.db.deps import get_db
from app.core.deps import get_current_user
from app.services import task_service
from app.models.user import User
from datetime import datetime

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskRead)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return task_service.create_task(db, user, task_in)


@router.get("/", response_model=list[TaskRead])
def read_tasks(
    status: StatusEnum | None = Query(default=None),
    due_from: datetime | None = Query(default=None),
    due_to: datetime | None = Query(default=None),
    tag_id: int | None = Query(default=None),
    sort_by_due_date: bool = Query(default=False),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return task_service.get_user_tasks(
        db,
        user,
        status=status,
        due_from=due_from,
        due_to=due_to,
        tag_id=tag_id,
        sort_by_due_date=sort_by_due_date,
    )


@router.get("/{task_id}", response_model=TaskRead)
def read_task(
    task_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    task = task_service.get_task_by_id(db, user, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return task_service.update_task(db, user, task_id, task_in)

@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    task_service.delete_task(db, user, task_id)
