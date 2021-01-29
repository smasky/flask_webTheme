"""empty message

Revision ID: 7187369a9ce1
Revises: 93ea044dce56
Create Date: 2019-10-16 19:13:49.578000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7187369a9ce1'
down_revision = '93ea044dce56'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('music',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('artist', sa.String(length=20), nullable=True),
    sa.Column('url', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_music'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('music')
    # ### end Alembic commands ###
