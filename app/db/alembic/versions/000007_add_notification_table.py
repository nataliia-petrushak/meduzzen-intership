"""Add notification table

Revision ID: 000007
Revises: 000006
Create Date: 2024-05-07 21:00:27.966836

"""
import uuid
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision: str = "000007"
down_revision: Union[str, None] = "000006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "notification",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("created_at", sa.DateTime(timezone=True), default=datetime.utcnow),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("user.id", ondelete="CASCADE"),
            nullable=False
        ),
        sa.Column(
            "quiz_id",
            UUID(as_uuid=True),
            sa.ForeignKey("quiz.id", ondelete="CASCADE"),
            nullable=False
        ),
        sa.Column("message", sa.String(500), nullable=False),
        sa.Column(
            "notification_status",
            ENUM("unread", "read", name="notification_status"), default="unread"
        ),
        sa.ForeignKeyConstraint(["quiz_id"], ["quiz.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
    )


def downgrade() -> None:
    op.drop_table("notification")
    op.execute("DROP TYPE status")
