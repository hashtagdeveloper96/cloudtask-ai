from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(
    db: Session,
    task_data: TaskCreate,
    user_id: int,
) -> Task:
    task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        user_id=user_id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_tasks(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 20,
    task_status: str | None = None,
    search: str | None = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
) -> list[Task]:
    query = select(Task).where(
        Task.user_id == user_id
    )

    if task_status:
        query = query.where(
            Task.status == task_status
        )

    if search:
        query = query.where(
            Task.title.ilike(
                f"%{search}%"
            )
        )

    sort_column = (
        Task.created_at
        if sort_by == "created_at"
        else Task.title
    )

    if sort_order == "asc":
        query = query.order_by(
            sort_column.asc()
        )
    else:
        query = query.order_by(
            sort_column.desc()
        )

    query = query.offset(skip).limit(limit)

    result = db.execute(query)

    return list(
        result.scalars().all()
    )


def get_task(
    db: Session,
    task_id: int,
    user_id: int,
) -> Task | None:
    result = db.execute(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id,
        )
    )

    return result.scalar_one_or_none()


def update_task(
    db: Session,
    task_id: int,
    task_data: TaskUpdate,
    user_id: int,
) -> Task | None:
    task = get_task(
        db=db,
        task_id=task_id,
        user_id=user_id,
    )

    if task is None:
        return None

    update_data = task_data.model_dump(
        exclude_unset=True,
    )

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    db: Session,
    task_id: int,
    user_id: int,
) -> bool:
    task = get_task(
        db=db,
        task_id=task_id,
        user_id=user_id,
    )

    if task is None:
        return False

    db.delete(task)
    db.commit()

    return True
