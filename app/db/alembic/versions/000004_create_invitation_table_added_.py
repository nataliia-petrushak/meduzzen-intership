"""Create invitation table & added relationships

Revision ID: 000004
Revises: 000003
Create Date: 2024-04-26 16:12:10.159490

"""
import uuid
from typing import Sequence, Union
from sqlalchemy import UUID
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

from app.db.models import Status

# revision identifiers, used by Alembic.
revision: str = "000004"
down_revision: Union[str, None] = "000003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "request",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("status", ENUM("INVITATION", "JOIN_REQUEST", "MEMBER", name="status"), nullable=False),
        sa.Column(
            "company_id",
            UUID(as_uuid=True),
            sa.ForeignKey("company.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "user_id", UUID(as_uuid=True), sa.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
        ),
        sa.ForeignKeyConstraint(["company_id"], ["company.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
    )


def downgrade() -> None:
    op.drop_table("invitation")
