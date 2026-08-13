"""
Functional tests for splent_feature_comments.

Functional tests use Flask's test client to exercise full HTTP
request/response cycles (GET, POST, redirects, rendered HTML).
"""

from splent_framework.db import db
from splent_io.splent_feature_comments.models import Comment
from splent_io.splent_feature_post.models import Post


def _disable_captcha(app):
    """Blank the Turnstile secret so no captcha listener vetoes the POST.

    The cloudflare feature defaults to Cloudflare's documented test keys, and
    a submission without a token is vetoed; these tests exercise comments,
    not the captcha.
    """
    previous = app.config.get("TURNSTILE_SECRET_KEY", "")
    app.config["TURNSTILE_SECRET_KEY"] = ""
    return previous


def _create_post(app):
    """A published post for comments to hang from (post_id is a real FK)."""
    with app.app_context():
        post = Post(title="Commented post", slug="commented-post", status="published")
        db.session.add(post)
        db.session.commit()
        return post.id


def test_create_without_fields_redirects_back(test_client):
    """POST /comments/<post_id> flashes and redirects when fields are missing."""
    response = test_client.post("/comments/1", data={})
    assert response.status_code == 302


def test_index_route_does_not_exist(test_client):
    """The feature exposes no comment listing page of its own."""
    response = test_client.get("/comments")
    assert response.status_code in (404, 405)


def test_create_holds_the_comment_for_moderation(test_client):
    """By default a fresh comment is stored unapproved, awaiting moderation."""
    app = test_client.application
    previous_secret = _disable_captcha(app)
    post_id = _create_post(app)
    try:
        response = test_client.post(
            f"/comments/{post_id}", data={"author_name": "Ana", "content": "Hola"}
        )
        assert response.status_code == 302
        with app.app_context():
            comment = Comment.query.filter_by(post_id=post_id).one()
            assert not comment.approved
    finally:
        app.config["TURNSTILE_SECRET_KEY"] = previous_secret


def test_auto_approve_publishes_immediately(test_client):
    """With auto_approve on (read at request time), the comment goes live at once."""
    app = test_client.application
    previous_secret = _disable_captcha(app)
    post_id = _create_post(app)
    original = app.config.get("COMMENTS_AUTO_APPROVE", False)
    app.config["COMMENTS_AUTO_APPROVE"] = True
    try:
        response = test_client.post(
            f"/comments/{post_id}", data={"author_name": "Ana", "content": "Hola"}
        )
        assert response.status_code == 302
        with app.app_context():
            comment = Comment.query.filter_by(post_id=post_id).one()
            assert comment.approved
    finally:
        app.config["COMMENTS_AUTO_APPROVE"] = original
        app.config["TURNSTILE_SECRET_KEY"] = previous_secret
