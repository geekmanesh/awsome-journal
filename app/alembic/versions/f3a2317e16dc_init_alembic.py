"""init alembic

Revision ID: f3a2317e16dc
Revises:
Create Date: 2026-05-19 10:21:57.396235

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "f3a2317e16dc"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
