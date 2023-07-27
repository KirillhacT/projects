"""erw

Revision ID: 08042b7b97a1
Revises: 412dadf942a1
Create Date: 2023-07-15 15:49:33.432241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08042b7b97a1'
down_revision = '412dadf942a1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hotels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('services', sa.JSON(), nullable=True),
    sa.Column('room_quantity', sa.Integer(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hotels')
    # ### end Alembic commands ###
