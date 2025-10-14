"""add content colum to post table

Revision ID: 8545246e6448
Revises: 13f0aa634f3c
Create Date: 2025-10-12 06:10:41.653785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8545246e6448'
down_revision: Union[str, Sequence[str], None] = '13f0aa634f3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    """Downgrade schema."""
    pass
