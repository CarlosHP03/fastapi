"""add content column to posts table

Revision ID: dc866ce2b8bb
Revises: a5fd0cd02a94
Create Date: 2024-12-16 18:23:32.213400

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc866ce2b8bb'
down_revision: Union[str, None] = 'a5fd0cd02a94'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))

    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')

    pass
