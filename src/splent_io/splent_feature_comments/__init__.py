from splent_framework.blueprints.base_blueprint import create_blueprint
from splent_framework.services.service_locator import register_service

from splent_io.splent_feature_comments.services import CommentsService

comments_bp = create_blueprint(__name__)


def init_feature(app):
    from splent_framework.assets.asset_registry import register_asset
    from splent_framework.settings.settings_schema import register_settings

    register_service(app, "CommentsService", CommentsService)
    register_asset(
        "css", "comments.assets", order=100, subfolder="css", filename="comments.css"
    )
    # Admin-configurable behaviour (framework renders the panel from this
    # schema).
    register_settings(
        "comments",
        "Comments",
        [
            {
                "key": "auto_approve",
                "type": "bool",
                "default": "0",
                "label": "Publish immediately",
                "help": "New comments appear without moderation. Off holds them for approval in the admin.",
            },
        ],
        icon="message-square",
    )


def inject_context_vars(app):
    return {}
