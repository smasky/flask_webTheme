"""empty message

Revision ID: 13d257d53a8e
Revises: c2b9a5e9c43b
Create Date: 2019-08-31 22:15:40.988000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13d257d53a8e'
down_revision = 'c2b9a5e9c43b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wei_admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('openid', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_wei_admin')),
    sa.UniqueConstraint('openid', name=op.f('uq_wei_admin_openid'))
    )
    op.create_table('weiitem',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('itembox_id', sa.Integer(), nullable=True),
    sa.Column('rank', sa.Integer(), nullable=True),
    sa.Column('answers', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['itembox_id'], ['itembox.id'], name=op.f('fk_weiitem_itembox_id_itembox')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_weiitem'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('weiitem')
    op.drop_table('wei_admin')
    # ### end Alembic commands ###
