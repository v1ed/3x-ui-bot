"""Add user access key

Revision ID: ef7d42fd0512
Revises: 1ace524bb006
Create Date: 2025-06-17 22:32:15.716030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef7d42fd0512'
down_revision: Union[str, Sequence[str], None] = '1ace524bb006'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_keys',
    sa.Column('key', sa.String(length=255), nullable=False),
    sa.Column('telegram_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['telegram_id'], ['users.telegram_id'], ),
    sa.PrimaryKeyConstraint('key'),
    sa.UniqueConstraint('key'),
    sa.UniqueConstraint('telegram_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_keys')
    # ### end Alembic commands ###
