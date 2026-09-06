from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:

    result = db.execute(
        select(User).where(
            User.email == email
        )
    )

    return result.scalar_one_or_none()


def get_user_by_username(
    db: Session,
    username: str,
) -> User | None:

    result = db.execute(
        select(User).where(
            User.username == username
        )
    )

    return result.scalar_one_or_none()


def create_user(
    db: Session,
    user_data: UserCreate,
) -> User:

    user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(
            user_data.password
        ),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
