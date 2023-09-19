"""add content column

Revision ID: 6799785481be
Revises: 597d6b6a725a
Create Date: 2023-09-19 01:36:51.908963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6799785481be'
down_revision: Union[str, None] = '597d6b6a725a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('content', sa.Text, nullable=False)
    )


def downgrade() -> None:
    op.drop_column('posts', 'content')
