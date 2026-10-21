def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_register_login(client):
    registered = client.post(
        "/api/auth/register",
        json={"username": "tester", "email": "tester@example.com", "password": "StrongPass123"},
    )
    assert registered.status_code == 201
    assert registered.get_json()["token"]

    logged_in = client.post(
        "/api/auth/login",
        json={"email": "tester@example.com", "password": "StrongPass123"},
    )
    assert logged_in.status_code == 200
    assert logged_in.get_json()["token"]


def test_register_validation(client):
    response = client.post("/api/auth/register", json={"email": "bad@example.com"})
    assert response.status_code == 400


def test_login_wrong_password(client, user):
    response = client.post(
        "/api/auth/login",
        json={"email": "user@example.com", "password": "wrong"},
    )
    assert response.status_code == 401


def test_public_events(client):
    response = client.get("/api/events")
    assert response.status_code == 200
    assert response.get_json() == []


def test_missing_event_returns_404(client):
    response = client.get("/api/events/99999")
    assert response.status_code == 404


def test_registration_requires_authentication(client):
    response = client.post("/api/events/99999/register")
    assert response.status_code == 401


def test_regular_user_cannot_create_event(client):
    registered = client.post(
        "/api/auth/register",
        json={"username": "regular", "email": "regular@example.com", "password": "StrongPass123"},
    )
    token = registered.get_json()["token"]
    response = client.post(
        "/api/events",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Доступная лекция"},
    )
    assert response.status_code == 403
