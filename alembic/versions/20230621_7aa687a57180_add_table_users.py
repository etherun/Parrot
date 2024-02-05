"""add_table_users_status

Revision ID: 7aa687a57180
Revises: 
Create Date: 2023-12-11 18:41:01.984114

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
        "users",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("username", sa.String(255), unique=True, nullable=False),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("is_admin", sa.Boolean, server_default=sa.text("false")),
        sa.Column("is_active", sa.Boolean, server_default=sa.text("true")),
        sa.Column("created_time", sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column("updated_time", sa.TIMESTAMP, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("users")
