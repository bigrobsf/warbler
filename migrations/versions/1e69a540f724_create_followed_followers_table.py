"""create followed_followers table

Revision ID: 1e69a540f724
Revises: 48d7c77d8d26
Create Date: 2017-10-25 11:03:35.519424

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e69a540f724'
down_revision = '48d7c77d8d26'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followed_followers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['users.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followed_followers')
    # ### end Alembic commands ###
