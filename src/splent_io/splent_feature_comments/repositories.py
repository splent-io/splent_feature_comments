from splent_io.splent_feature_comments.models import Comment
from splent_framework.repositories.BaseRepository import BaseRepository


class CommentsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Comment)
