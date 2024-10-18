import pytest
from flask import session

from app import create_app
from config import TestingConfig


@pytest.fixture
def client():
    app = create_app(TestingConfig)
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for testing
    with app.test_client() as client:
        yield client


def test_home_route_without_cookie(client):
    response = client.get("/")
    assert response.status_code == 302
    assert response.headers["Location"] == "/login"


def test_home_route_with_cookie(client):
    client.set_cookie("localhost", "username", "John_Doe")
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome, John_Doe" in response.data
    assert b'href="/profile"' in response.data


def test_login_route_get(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"<form" in response.data
    assert b'name="username"' in response.data


def test_login_route_post_valid(client):
    response = client.post(
        "/login", data={"username": "John_Doe"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Welcome, John_Doe" in response.data
    assert b"You have visited this page 1 time(s)" in response.data


def test_login_route_post_invalid(client):
    response = client.post("/login", data={"username": "invalid_username"})
    assert response.status_code == 200
    assert b"Username must be in the format Firstname_Lastname" in response.data


def test_profile_route_without_cookie(client):
    response = client.get("/profile")
    assert response.status_code == 302
    assert response.headers["Location"] == "/login"


def test_profile_route_with_cookie(client):
    client.set_cookie("localhost", "username", "John_Doe")
    with client.session_transaction() as sess:
        sess["visit_count"] = 2
    response = client.get("/profile")
    assert response.status_code == 200
    assert b"Welcome, John_Doe" in response.data
    assert b"You have visited this page 3 time(s)" in response.data


def test_logout_route(client):
    client.set_cookie("localhost", "username", "John_Doe")
    with client.session_transaction() as sess:
        sess["visit_count"] = 2
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data
    assert "username" not in client.get_cookie("localhost")
    with client.session_transaction() as sess:
        assert "visit_count" not in sess


def test_logout_clears_session_and_cookie(client):
    # Set up a logged-in user
    client.post("/login", data={"username": "John_Doe"})

    # Verify user is logged in
    response = client.get("/profile")
    assert response.status_code == 200
    assert b"Welcome, John_Doe" in response.data

    # Logout
    response = client.get("/logout", follow_redirects=True)

    # Check if redirected to login page
    assert response.status_code == 200
    assert b"Login" in response.data

    # Verify cookie is cleared
    assert "username" not in client.get_cookie("localhost")

    # Verify session is cleared
    with client.session_transaction() as sess:
        assert "visit_count" not in sess


def test_visit_count_resets_after_logout_login(client):
    # Login and visit profile twice
    client.post("/login", data={"username": "John_Doe"})
    client.get("/profile")
    response = client.get("/profile")
    assert b"You have visited this page 2 time(s)" in response.data

    # Logout
    client.get("/logout")

    # Login again and check visit count
    client.post("/login", data={"username": "John_Doe"})
    response = client.get("/profile")
    assert b"You have visited this page 1 time(s)" in response.data


def test_multiple_users_independent_visit_counts(client):
    # Login as first user and visit profile
    client.post("/login", data={"username": "John_Doe"})
    client.get("/profile")
    client.get("/profile")
    response = client.get("/profile")
    assert b"You have visited this page 3 time(s)" in response.data

    # Logout first user
    client.get("/logout")

    # Login as second user and visit profile
    client.post("/login", data={"username": "Jane_Smith"})
    response = client.get("/profile")
    assert b"You have visited this page 1 time(s)" in response.data

    # Logout second user
    client.get("/logout")

    # Login as first user again and check visit count
    client.post("/login", data={"username": "John_Doe"})
    response = client.get("/profile")
    assert b"You have visited this page 1 time(s)" in response.data
