"""empty message

Revision ID: d4c15f7eb04b
Revises: 08764d035684
Create Date: 2021-05-27 13:35:06.749560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4c15f7eb04b'
down_revision = '08764d035684'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('User', sa.Column('aadhar_card_no', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('User', 'aadhar_card_no')
    # ### end Alembic commands ###