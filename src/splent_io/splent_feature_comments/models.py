from datetime import datetime

from splent_framework.db import db


class Comment(db.Model):
    """A comment on a post. New comments start unapproved (moderation)."""

    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey("post.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    author_name = db.Column(db.String(128), nullable=False)
    author_email = db.Column(db.String(255), default="")
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    approved = db.Column(db.Boolean, default=False, index=True)

    def __repr__(self):
        return f"Comment<{self.id} on post {self.post_id}>"
