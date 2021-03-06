"""change number of pages nullable on True

Revision ID: 1c7ad1b3e599
Revises: e5e94ed52c10
Create Date: 2022-01-30 12:12:28.135987

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "1c7ad1b3e599"
down_revision = "e5e94ed52c10"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "books",
        "number_of_pages",
        existing_type=mysql.INTEGER(),
        nullable=True,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "books",
        "number_of_pages",
        existing_type=mysql.INTEGER(),
        nullable=False,
    )
    # ### end Alembic commands ###
