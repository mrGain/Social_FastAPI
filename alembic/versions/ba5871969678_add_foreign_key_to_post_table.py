"""add foreign-key to post table

Revision ID: ba5871969678
Revises: e591e7c00c4b
Create Date: 2023-09-19 02:43:41.270387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba5871969678'
down_revision: Union[str, None] = 'e591e7c00c4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('owner_id', sa.Integer, nullable=False)
    )
    op.create_foreign_key(
        'posts_users_fk',
        source_table='posts',
        referent_table='users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    op.drop_constraint(
        'posts_users_fk',
        table_name='posts'
    )
    op.drop_column(
        'posts',
        'owner_id'
    )
