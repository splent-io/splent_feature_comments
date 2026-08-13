"""
comments feature configuration.

Injects environment variables into Flask app.config.
Add your feature's env vars here so the framework can track them.

To regenerate from source code: splent feature:inject-config splent_feature_comments
"""

import os


def inject_config(app):
    app.config.update(
        {
            # Publish new comments immediately instead of holding them for
            # moderation. Off unless the product asks for it. Also
            # admin-editable in the settings panel, which wins at request time.
            "COMMENTS_AUTO_APPROVE": os.getenv("COMMENTS_AUTO_APPROVE", "")
            .strip()
            .lower()
            in ("1", "true", "yes"),
        }
    )
