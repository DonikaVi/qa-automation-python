import pytest
from jsonschema import validate

pytestmark = pytest.mark.api

POST_SCHEMA = {
    "type": "object",
    "required": ["userId", "id", "title", "body"],
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
    },
}


def url(api, path: str) -> str:
    return f"{api.base_url}{path}"


@pytest.mark.smoke
def test_get_posts_list(api):
    r = api.get(url(api, "/posts"), timeout=10)
    assert r.status_code == 200
    assert len(r.json()) == 100


@pytest.mark.parametrize("post_id", [1, 50, 100])
def test_get_single_post_matches_schema(api, post_id):
    r = api.get(url(api, f"/posts/{post_id}"), timeout=10)
    assert r.status_code == 200
    body = r.json()
    validate(body, POST_SCHEMA)
    assert body["id"] == post_id


def test_get_unknown_post_returns_404(api):
    r = api.get(url(api, "/posts/99999"), timeout=10)
    assert r.status_code == 404


def test_filter_posts_by_user(api):
    r = api.get(url(api, "/posts"), params={"userId": 1}, timeout=10)
    assert r.status_code == 200
    assert r.json() and all(p["userId"] == 1 for p in r.json())


def test_create_post(api):
    payload = {"title": "qa", "body": "hello", "userId": 1}
    r = api.post(url(api, "/posts"), json=payload, timeout=10)
    assert r.status_code == 201
    assert r.json()["title"] == "qa"
    assert "id" in r.json()


def test_response_time_is_reasonable(api):
    r = api.get(url(api, "/posts/1"), timeout=10)
    assert r.elapsed.total_seconds() < 2
