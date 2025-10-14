"""add user table

Revision ID: c60c87c6edd9
Revises: 8545246e6448
Create Date: 2025-10-12 06:19:01.785299

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c60c87c6edd9"
down_revision: Union[str, Sequence[str], None] = "8545246e6448"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_table('users')
    """Downgrade schema."""
    pass
