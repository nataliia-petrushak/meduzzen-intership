from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID

"""create user table
Revision ID: 000001
Revises: 
Create Date: 2024-04-12 15:35:11.855991
"""

revision: str = "000001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("username", sa.String(20), nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(50), unique=True, nullable=False),
        sa.Column("password", sa.String(50), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("user")
