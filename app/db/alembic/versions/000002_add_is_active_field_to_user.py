"""Add is_active field to user

Revision ID: 000002
Revises: 000001
Create Date: 2024-04-24 20:42:55.929513

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "000002"
down_revision: Union[str, None] = "000001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("user", sa.Column("is_active", sa.Boolean(), default=True))


def downgrade() -> None:
    op.drop_column("user", "is_active")
