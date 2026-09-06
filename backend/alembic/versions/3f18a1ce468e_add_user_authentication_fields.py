
"""add user authentication fields

Revision ID: 3f18a1ce468e
Revises:
Create Date: 2026-09-02

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3f18a1ce468e"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Add authentication fields to users
    op.add_column(
        "users",
        sa.Column("username", sa.String(length=100), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column("hashed_password", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=True,
            server_default=sa.true(),
        ),
    )

    # Populate new fields for any existing users
    op.execute(
        """
        UPDATE users
        SET username = 'legacy_user_' || id
        WHERE username IS NULL
        """
    )

    op.execute(
        """
        UPDATE users
        SET hashed_password = 'LEGACY_USER_NO_LOGIN'
        WHERE hashed_password IS NULL
        """
    )

    # Make authentication columns required
    op.alter_column(
        "users",
        "username",
        existing_type=sa.String(length=100),
        nullable=False,
    )

    op.alter_column(
        "users",
        "hashed_password",
        existing_type=sa.String(length=255),
        nullable=False,
    )

    op.alter_column(
        "users",
        "is_active",
        existing_type=sa.Boolean(),
        nullable=False,
    )

    op.create_index(
        op.f("ix_users_username"),
        "users",
        ["username"],
        unique=True,
    )

    # Add user_id as nullable first
    op.add_column(
        "tasks",
        sa.Column("user_id", sa.Integer(), nullable=True),
    )

    # Create a special migration user only when tasks exist
    # and there are no users yet.
    op.execute(
        """
        INSERT INTO users (
            email,
            username,
            hashed_password,
            is_active,
            created_at
        )
        SELECT
            'legacy@cloudtask.local',
            'legacy_user',
            'LEGACY_USER_NO_LOGIN',
            FALSE,
            CURRENT_TIMESTAMP
        WHERE EXISTS (
            SELECT 1 FROM tasks
        )
        AND NOT EXISTS (
            SELECT 1 FROM users
        )
        """
    )

    # Assign existing tasks to the first available user
    op.execute(
        """
        UPDATE tasks
        SET user_id = (
            SELECT id
            FROM users
            ORDER BY id
            LIMIT 1
        )
        WHERE user_id IS NULL
        """
    )

    # Now user_id can safely become NOT NULL
    op.alter_column(
        "tasks",
        "user_id",
        existing_type=sa.Integer(),
        nullable=False,
    )

    op.create_index(
        op.f("ix_tasks_user_id"),
        "tasks",
        ["user_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_tasks_user_id_users",
        "tasks",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
