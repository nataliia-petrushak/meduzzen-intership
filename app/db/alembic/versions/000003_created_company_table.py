"""Created company table

Revision ID: 000003
Revises: 000002
Create Date: 2024-04-25 20:14:48.701913

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID


# revision identifiers, used by Alembic.
revision: str = "000003"
down_revision: Union[str, None] = "000002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "company",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column(
            "owner_id", UUID(as_uuid=True), sa.ForeignKey("user.id"), nullable=False
        ),
        sa.Column("description", sa.String(500)),
        sa.Column("is_hidden", sa.Boolean(), default=False),
        sa.ForeignKeyConstraint(["owner_id"], ["user.id"]),
    )


def downgrade() -> None:
    op.drop_table("company")
