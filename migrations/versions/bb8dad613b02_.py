"""empty message

Revision ID: bb8dad613b02
Revises: 2c33d1a94f16
Create Date: 2019-09-01 15:52:53.228000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb8dad613b02'
down_revision = '2c33d1a94f16'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('weiadmin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('truename', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('username', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('year', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('weiadmin', schema=None) as batch_op:
        batch_op.drop_column('year')
        batch_op.drop_column('username')
        batch_op.drop_column('truename')

    # ### end Alembic commands ###
