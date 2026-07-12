"""rename todos to tasks

Revision ID: 81b695beef3f
Revises: 6ae548c7edec
Create Date: 2026-07-12 12:18:48.729727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '81b695beef3f'
down_revision: Union[str, Sequence[str], None] = '6ae548c7edec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # autogenerate can't detect renames (it would emit drop+create and lose data),
    # so this is hand-written using rename operations instead.
    op.rename_table("todos", "tasks")
    op.execute("ALTER SEQUENCE todos_id_seq RENAME TO tasks_id_seq")
    op.execute("ALTER INDEX ix_todos_id RENAME TO ix_tasks_id")
    op.execute("ALTER TABLE tasks RENAME CONSTRAINT todos_pkey TO tasks_pkey")
    op.execute(
        "ALTER TABLE tasks RENAME CONSTRAINT todos_list_id_fkey TO tasks_list_id_fkey"
    )
    op.execute(
        "ALTER TABLE tasks RENAME CONSTRAINT todos_owner_id_fkey TO tasks_owner_id_fkey"
    )

    op.alter_column("repeats", "todo_id", new_column_name="task_id")
    op.execute(
        "ALTER TABLE repeats RENAME CONSTRAINT repeats_todo_id_fkey TO repeats_task_id_fkey"
    )
    op.execute(
        "ALTER TABLE repeats RENAME CONSTRAINT repeats_todo_id_key TO repeats_task_id_key"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "ALTER TABLE repeats RENAME CONSTRAINT repeats_task_id_key TO repeats_todo_id_key"
    )
    op.execute(
        "ALTER TABLE repeats RENAME CONSTRAINT repeats_task_id_fkey TO repeats_todo_id_fkey"
    )
    op.alter_column("repeats", "task_id", new_column_name="todo_id")

    op.execute(
        "ALTER TABLE tasks RENAME CONSTRAINT tasks_owner_id_fkey TO todos_owner_id_fkey"
    )
    op.execute(
        "ALTER TABLE tasks RENAME CONSTRAINT tasks_list_id_fkey TO todos_list_id_fkey"
    )
    op.execute("ALTER TABLE tasks RENAME CONSTRAINT tasks_pkey TO todos_pkey")
    op.execute("ALTER INDEX ix_tasks_id RENAME TO ix_todos_id")
    op.execute("ALTER SEQUENCE tasks_id_seq RENAME TO todos_id_seq")
    op.rename_table("tasks", "todos")
