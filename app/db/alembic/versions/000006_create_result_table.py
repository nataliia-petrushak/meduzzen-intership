"""create result table

Revision ID: 000006
Revises: 000005
Create Date: 2024-05-01 19:51:46.404162

"""

import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision: str = "000006"
down_revision: Union[str, None] = "000005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "result",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column(
            "user_id",
            UUID(as_uuid=True),
            sa.ForeignKey("user.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "quiz_id",
            UUID(as_uuid=True),
            sa.ForeignKey("quiz.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "company_id",
            UUID(as_uuid=True),
            sa.ForeignKey("company.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("all_results", sa.MutableList.as_mutable(JSONB()), nullable=False),
        sa.ForeignKeyConstraint(["company_id"], ["company.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.ForeignKeyConstraint(["quiz_id"], ["quiz.id"]),
    )


def downgrade() -> None:
    op.drop_table("result")
