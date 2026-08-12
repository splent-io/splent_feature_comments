"""
Functional tests for splent_feature_comments.

Functional tests use Flask's test client to exercise full HTTP
request/response cycles (GET, POST, redirects, rendered HTML).
"""


def test_create_without_fields_redirects_back(test_client):
    """POST /comments/<post_id> flashes and redirects when fields are missing."""
    response = test_client.post("/comments/1", data={})
    assert response.status_code == 302


def test_index_route_does_not_exist(test_client):
    """The feature exposes no comment listing page of its own."""
    response = test_client.get("/comments")
    assert response.status_code in (404, 405)
