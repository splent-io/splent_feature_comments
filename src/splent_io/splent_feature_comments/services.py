from splent_io.splent_feature_comments.models import Comment
from splent_io.splent_feature_comments.repositories import CommentsRepository
from splent_framework.services.BaseService import BaseService


class CommentsService(BaseService):
    def __init__(self):
        super().__init__(CommentsRepository())

    def approved_for(self, post_id):
        return (
            Comment.query.filter_by(post_id=post_id, approved=True)
            .order_by(Comment.created_at.asc())
            .all()
        )

    def pending(self):
        return (
            Comment.query.filter_by(approved=False)
            .order_by(Comment.created_at.desc())
            .all()
        )

    def all_comments(self):
        return Comment.query.order_by(Comment.created_at.desc()).all()
