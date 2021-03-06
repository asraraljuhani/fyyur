"""empty message

Revision ID: 5256dc25ce5d
Revises: 18fb4a62b067
Create Date: 2021-06-17 15:42:02.786674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5256dc25ce5d'
down_revision = '18fb4a62b067'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('website_link', sa.String(length=120), nullable=True))
    op.drop_column('artist', 'website')
    op.add_column('venue', sa.Column('website_link', sa.String(length=120), nullable=True))
    op.drop_column('venue', 'website')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('website', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.drop_column('venue', 'website_link')
    op.add_column('artist', sa.Column('website', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.drop_column('artist', 'website_link')
    # ### end Alembic commands ###
