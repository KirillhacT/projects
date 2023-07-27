"""fds

Revision ID: b3d2ee5d7001
Revises: 5883fa107917
Create Date: 2023-07-27 14:32:03.234078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3d2ee5d7001'
down_revision = '5883fa107917'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=40), nullable=False),
    sa.Column('release_date', sa.Date(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('series_count', sa.Integer(), nullable=False),
    sa.Column('genre_id', sa.String(length=20), nullable=True),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('test')
    op.drop_constraint('genres_title_key', 'genres', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('genres_title_key', 'genres', ['title'])
    op.create_table('test',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('code', sa.VARCHAR(length=4), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='test_pkey')
    )
    op.drop_table('posts')
    op.drop_table('users')
    # ### end Alembic commands ###
