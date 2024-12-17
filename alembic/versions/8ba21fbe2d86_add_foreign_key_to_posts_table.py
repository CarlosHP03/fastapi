"""add foreign-key to posts table

Revision ID: 8ba21fbe2d86
Revises: e0140178317a
Create Date: 2024-12-17 10:01:27.741313

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ba21fbe2d86'
down_revision: Union[str, None] = 'e0140178317a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['user_id'], 
                          remote_cols=['id'], ondelete="CASCADE")
    
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')

    pass
