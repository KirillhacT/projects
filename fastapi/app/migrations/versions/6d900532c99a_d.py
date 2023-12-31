"""d

Revision ID: 6d900532c99a
Revises: 718362f256a1
Create Date: 2023-07-27 14:13:15.621461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d900532c99a'
down_revision = '718362f256a1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test')
    op.drop_constraint('posts_genre_fkey', 'posts', type_='foreignkey')
    op.drop_column('posts', 'genre')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('genre', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
    op.create_foreign_key('posts_genre_fkey', 'posts', 'genres', ['genre'], ['title'])
    op.create_table('test',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('code', sa.VARCHAR(length=4), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='test_pkey')
    )
    # ### end Alembic commands ###
