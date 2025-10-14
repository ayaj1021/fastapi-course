"""add last few columns to posts table

Revision ID: 1fe39a0f1323
Revises: db187fef52cd
Create Date: 2025-10-13 05:23:25.113747

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1fe39a0f1323"
down_revision: Union[str, Sequence[str], None] = "db187fef52cd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("Now()"),
        ),
    )
    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    """Downgrade schema."""
    pass
