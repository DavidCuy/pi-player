"""initial db diagram

Revision ID: 7d05ab9ac7ea
Revises: 
Create Date: 2022-06-12 02:17:47.480441

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d05ab9ac7ea'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('playlists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('order_file', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('videos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('video_file', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('format', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rel_video_playlist',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_video', sa.Integer(), nullable=True),
    sa.Column('id_playlist', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_playlist'], ['playlists.id'], ),
    sa.ForeignKeyConstraint(['id_video'], ['videos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('schedules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_playlist', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('start', sa.Time(), nullable=False),
    sa.Column('description', sa.Time(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('days', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['id_playlist'], ['playlists.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('schedules')
    op.drop_table('rel_video_playlist')
    op.drop_table('videos')
    op.drop_table('playlists')
    # ### end Alembic commands ###
