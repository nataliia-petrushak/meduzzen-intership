"""create quiz table

Revision ID: 000005
Revises: 000004
Create Date: 2024-05-01 15:50:19.222687

"""

import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableList

# revision identifiers, used by Alembic.
revision: str = "000005"
down_revision: Union[str, None] = "000004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "quiz",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.String(500)),
        sa.Column("num_done", sa.Integer(), default=0),
        sa.Column(
            "company_id",
            UUID(as_uuid=True),
            sa.ForeignKey("company.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("questions", MutableList.as_mutable(JSONB()), nullable=False),
        sa.ForeignKeyConstraint(["company_id"], ["company.id"]),
    )


def downgrade() -> None:
    op.drop_table("quiz")
