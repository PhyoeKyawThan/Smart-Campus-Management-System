"""new table added

Revision ID: 418bc970ed27
Revises: 
Create Date: 2024-05-15 14:55:22.052525

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '418bc970ed27'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stuff', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nrc', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stuff', schema=None) as batch_op:
        batch_op.drop_column('nrc')

    # ### end Alembic commands ###