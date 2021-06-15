"""empty message

Revision ID: 584f3ba5268f
Revises: 7335aa50b55c
Create Date: 2021-06-15 14:04:02.655768

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '584f3ba5268f'
down_revision = '7335aa50b55c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('show',
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
    sa.PrimaryKeyConstraint('artist_id', 'venue_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('show')
    # ### end Alembic commands ###
