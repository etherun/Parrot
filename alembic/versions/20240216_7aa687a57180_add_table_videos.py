"""add_table_videos

Revision ID: 7aa687a57180
Revises: 
Create Date: 2024-2-16 18:06:01.988888

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7aa687a57180"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "videos",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("checksum", sa.Text, unique=True, nullable=False),
        sa.Column("text", sa.Text, nullable=True),
        sa.Column("text_analysis", sa.ARRAY(sa.JSON), nullable=True),
        sa.Column("emotion", sa.ARRAY(sa.JSON), nullable=True),
        sa.Column("created_time", sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column("updated_time", sa.TIMESTAMP, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("videos")
