"""create user table

Revision ID: 60a4739343d6
Revises: 294fdd69d3f8
Create Date: 2024-04-12 14:42:58.388570

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "60a4739343d6"
down_revision: Union[str, None] = "294fdd69d3f8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", autoincrement=True, unique=True, primary_key=True),
        sa.Column("username", sa.String(20), unique=True, nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(50), unique=True, nullable=False),
        sa.Column("password", sa.String(50), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("user")
