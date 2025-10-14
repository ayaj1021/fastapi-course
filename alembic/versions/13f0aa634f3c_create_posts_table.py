"""Create posts table

Revision ID: 13f0aa634f3c
Revises:
Create Date: 2025-10-12 05:52:34.489692

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "13f0aa634f3c"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.INTEGER(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )
    # """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_table('posts')
    """Downgrade schema."""
    pass
