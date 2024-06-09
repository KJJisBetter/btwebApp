"""Increase length of password_hash column

Revision ID: 8396ea953e11
Revises: 68fd154f2458
Create Date: 2024-06-09 18:13:01.106832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8396ea953e11'
down_revision = '68fd154f2458'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.String(length=1024),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=128),
               existing_nullable=True)

    # ### end Alembic commands ###
