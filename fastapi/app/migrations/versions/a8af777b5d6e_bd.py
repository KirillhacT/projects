"""bd

Revision ID: a8af777b5d6e
Revises: 5b639bf9601b
Create Date: 2023-07-23 11:07:52.229947

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a8af777b5d6e'
down_revision = '5b639bf9601b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=40), nullable=False),
    sa.Column('release_date', sa.Date(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('series_count', sa.Integer(), nullable=False),
    sa.Column('genre', sa.String(length=20), nullable=False),
    sa.Column('image', sa.LargeBinary(), nullable=True),
    sa.ForeignKeyConstraint(['genre'], ['genres.title'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('progress')
    op.drop_table('rooms')
    op.drop_table('hotels')
    op.drop_table('students')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('students',
    sa.Column('record_book', sa.NUMERIC(precision=5, scale=0), autoincrement=False, nullable=False),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('doc_ser', sa.NUMERIC(precision=4, scale=0), autoincrement=False, nullable=True),
    sa.Column('doc_num', sa.NUMERIC(precision=6, scale=0), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('record_book', name='students_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('hotels',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('hotels_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('location', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('services', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('room_quantity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('image_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='hotels_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('rooms',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('hotel_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('services', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('image_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], name='rooms_hotel_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='rooms_pkey')
    )
    op.create_table('progress',
    sa.Column('record_book', sa.NUMERIC(precision=5, scale=0), autoincrement=False, nullable=False),
    sa.Column('subject', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('acad_year', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('term', sa.NUMERIC(precision=1, scale=0), autoincrement=False, nullable=False),
    sa.Column('mark', sa.NUMERIC(precision=1, scale=0), server_default=sa.text('5'), autoincrement=False, nullable=False),
    sa.CheckConstraint('mark >= 3::numeric AND mark <= 5::numeric', name='progress_mark_check'),
    sa.CheckConstraint('term = 1::numeric OR term = 2::numeric', name='progress_term_check'),
    sa.ForeignKeyConstraint(['record_book'], ['students.record_book'], name='progress_record_book_fkey', onupdate='CASCADE', ondelete='CASCADE')
    )
    op.drop_table('posts')
    op.drop_table('genres')
    # ### end Alembic commands ###
