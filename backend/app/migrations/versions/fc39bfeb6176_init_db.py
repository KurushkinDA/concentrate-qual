"""init db

Revision ID: fc39bfeb6176
Revises:
Create Date: 2025-05-06 13:51:28.873454

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fc39bfeb6176"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)
    op.create_table(
        "concentrates",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("iron", sa.Float(), nullable=False),
        sa.Column("silicon", sa.Float(), nullable=False),
        sa.Column("aluminum", sa.Float(), nullable=False),
        sa.Column("calcium", sa.Float(), nullable=False),
        sa.Column("sulfur", sa.Float(), nullable=False),
        sa.Column("report_month", sa.String(length=7), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_concentrates_id"), "concentrates", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_concentrates_id"), table_name="concentrates")
    op.drop_table("concentrates")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###
