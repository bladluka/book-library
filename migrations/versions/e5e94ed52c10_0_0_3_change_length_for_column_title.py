"""change length for column title

Revision ID: e5e94ed52c10
Revises: ae2f6db54be3
Create Date: 2022-01-30 11:56:33.646136

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "e5e94ed52c10"
down_revision = "ae2f6db54be3"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "books",
        "title",
        existing_type=mysql.VARCHAR(length=50),
        type_=sa.String(length=100),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "books",
        "title",
        existing_type=sa.String(length=100),
        type_=mysql.VARCHAR(length=50),
        existing_nullable=False,
    )
    # ### end Alembic commands ###