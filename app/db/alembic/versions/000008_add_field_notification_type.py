"""add field notification_type

Revision ID: 000008
Revises: 000007
Create Date: 2024-05-09 17:02:12.092774

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision: str = "000008"
down_revision: Union[str, None] = "000007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "notification",
        sa.Column(
            "notification_type",
            ENUM("new_quiz", "reminder", name="notification_type"), default="new_quiz")
    )


def downgrade() -> None:
    op.drop_column("notification", "notification_type")
    op.execute("DROP TYPE notification_type")
