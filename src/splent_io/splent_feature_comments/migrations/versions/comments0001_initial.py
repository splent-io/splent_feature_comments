"""comment table.

Revision ID: comments0001
Revises:
"""

import sqlalchemy as sa
from alembic import op

revision = "comments0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "comment",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("author_name", sa.String(length=128), nullable=False),
        sa.Column("author_email", sa.String(length=255), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("approved", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(["post_id"], ["post.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_comment_post_id"), "comment", ["post_id"], unique=False)
    op.create_index(
        op.f("ix_comment_created_at"), "comment", ["created_at"], unique=False
    )
    op.create_index(op.f("ix_comment_approved"), "comment", ["approved"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_comment_approved"), table_name="comment")
    op.drop_index(op.f("ix_comment_created_at"), table_name="comment")
    op.drop_index(op.f("ix_comment_post_id"), table_name="comment")
    op.drop_table("comment")
