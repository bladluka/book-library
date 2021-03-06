"""authors_table

Revision ID: 4193770d402b
Revises:
Create Date: 2022-01-26 00:02:26.988179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4193770d402b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "first_and_last_name", sa.String(length=100), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("authors")
    # ### end Alembic commands ###
