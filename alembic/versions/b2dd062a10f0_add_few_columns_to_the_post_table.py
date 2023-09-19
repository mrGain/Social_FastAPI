"""add few columns to the post table

Revision ID: b2dd062a10f0
Revises: ba5871969678
Create Date: 2023-09-19 02:59:42.567795

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2dd062a10f0'
down_revision: Union[str, None] = 'ba5871969678'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean, nullable=True, default=True)
    )
    op.add_column(
        'posts',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False)
    )
    
def downgrade() -> None:
    op.drop_column(
        'posts',
        'published'
    )
    op.drop_column(
        'posts',
        'created_at'
    )
