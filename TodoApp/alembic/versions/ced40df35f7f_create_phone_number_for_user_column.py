"""Create phone number for user column

Revision ID: ced40df35f7f
Revises: 
Create Date: 2025-11-08 15:04:35.145815

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ced40df35f7f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(length=20), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'phone_number')
