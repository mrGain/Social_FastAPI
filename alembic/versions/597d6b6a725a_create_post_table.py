"""create post table.

Revision ID: 597d6b6a725a
Revises: 
Create Date: 2023-09-19 00:30:42.824541

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '597d6b6a725a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(255), nullable=False)
    )
    


def downgrade() -> None:
    op.drop_table('posts')

