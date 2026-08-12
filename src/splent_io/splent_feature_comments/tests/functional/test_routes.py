"""
Functional tests for splent_feature_comments.

Functional tests use Flask's test client to exercise full HTTP
request/response cycles (GET, POST, redirects, rendered HTML).
"""


def test_create_unknown_post_is_404(test_client):
    """The only public route is POST /comments/<post_id>; a missing post 404s."""
    response = test_client.post(
        "/comments/999999",
        data={"author_name": "Someone", "content": "Hello"},
    )
    assert response.status_code == 404


def test_index_route_does_not_exist(test_client):
    """The feature exposes no comment listing page of its own."""
    response = test_client.get("/comments")
    assert response.status_code in (404, 405)
