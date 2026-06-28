from splent_framework.blueprints.base_blueprint import create_blueprint
from splent_framework.services.service_locator import register_service

from splent_io.splent_feature_comments.services import CommentsService

comments_bp = create_blueprint(__name__)


def init_feature(app):
    from splent_framework.assets.asset_registry import register_asset

    register_service(app, "CommentsService", CommentsService)
    register_asset(
        "css", "comments.assets", order=100, subfolder="css", filename="comments.css"
    )


def inject_context_vars(app):
    return {}
