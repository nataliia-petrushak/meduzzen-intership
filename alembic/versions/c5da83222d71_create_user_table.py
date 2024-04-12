"""create user table

Revision ID: c5da83222d71
Revises: 
Create Date: 2024-04-12 15:35:11.855991

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c5da83222d71"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column(
            "id",
            sa.Integer,
            autoincrement=True,
            unique=True,
            primary_key=True,
            nullable=False,
        ),
        sa.Column("username", sa.String(20), unique=True, nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(50), unique=True, nullable=False),
        sa.Column("password", sa.String(50), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("user")
