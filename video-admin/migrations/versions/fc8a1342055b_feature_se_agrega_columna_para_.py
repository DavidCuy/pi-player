"""feature: se agrega columna para identificar repetidos

Revision ID: fc8a1342055b
Revises: f0091162eba8
Create Date: 2022-06-20 00:03:40.608542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc8a1342055b'
down_revision = 'f0091162eba8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('schedules', schema=None) as batch_op:
        batch_op.add_column(sa.Column('repeat', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('schedules', schema=None) as batch_op:
        batch_op.drop_column('repeat')

    # ### end Alembic commands ###