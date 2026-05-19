"""add phone_number column

Revision ID: c3515e1327fa
Revises: f3a2317e16dc
Create Date: 2026-05-19 10:24:05.571238

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c3515e1327fa"
down_revision: Union[str, Sequence[str], None] = "f3a2317e16dc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("phone_number", sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "phone_number")
