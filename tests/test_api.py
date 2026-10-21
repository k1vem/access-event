<<<<<<< HEAD
def _register_and_login(client, email, role="user"):
    client.post("/api/register", json={"username": email.split("@")[0], "email": email, "password": "Passw0rd!", "role": role})
    resp = client.post("/api/login", json={"email": email, "password": "Passw0rd!"})
    return resp.get_json()["token"]

def test_register_success(client):
    resp = client.post("/api/register", json={"username": "anna", "email": "anna@mail.ru", "password": "Passw0rd!", "role": "user"})
    assert resp.status_code == 201 and "user_id" in resp.get_json()

def test_register_invalid_email_rejected(client):
    resp = client.post("/api/register", json={"username": "bob", "email": "not-an-email", "password": "Passw0rd!", "role": "user"})
    assert resp.status_code == 400

def test_login_returns_token(client):
    client.post("/api/register", json={"username": "org", "email": "org@mail.ru", "password": "Passw0rd!", "role": "organizer"})
    resp = client.post("/api/login", json={"email": "org@mail.ru", "password": "Passw0rd!"})
    assert resp.status_code == 200 and "token" in resp.get_json()

def test_create_event_requires_organizer_token(client):
    resp = client.post("/api/events", json={"title": "Лекция"})
    assert resp.status_code in (401, 403)

def test_events_list_public(client):
    resp = client.get("/api/events")
    assert resp.status_code == 200

def test_create_event_with_token(client):
    token = _register_and_login(client, "org3@mail.ru", role="organizer")
    resp = client.post("/api/events", json={"title": "Тихий кинопросмотр", "event_date": "2026-11-03 19:00:00", "is_inclusive": True}, headers={"Authorization": "Bearer " + token})
    assert resp.status_code == 201 and "id" in resp.get_json()

def test_register_for_event(client):
    org_token = _register_and_login(client, "org4@mail.ru", role="organizer")
    client.post("/api/events", json={"title": "Экскурсия", "event_date": "2026-11-03 12:00:00"}, headers={"Authorization": "Bearer " + org_token})
    events = client.get("/api/events").get_json(); event_id = events[0]["id"]
    user_token = _register_and_login(client, "p3@mail.ru", role="user")
    resp = client.post("/api/registrations", json={"event_id": event_id}, headers={"Authorization": "Bearer " + user_token})
    assert resp.status_code == 201 and resp.get_json()["status"] == "pending"

def test_my_registrations_list(client):
    token = _register_and_login(client, "p4@mail.ru", role="user")
    resp = client.get("/api/registrations", headers={"Authorization": "Bearer " + token})
    assert resp.status_code == 200
=======
def test_health(client):
    r=client.get("/health"); assert r.status_code==200 and r.get_json()["status"]=="ok"
def test_register_login(client):
    r=client.post("/api/auth/register",json={"username":"tester","email":"tester@example.com","password":"StrongPass123"}); assert r.status_code==201
    r=client.post("/api/auth/login",json={"email":"tester@example.com","password":"StrongPass123"}); assert r.status_code==200 and r.get_json()["token"]
def test_register_validation(client): assert client.post("/api/auth/register",json={"email":"bad@example.com"}).status_code==400
def test_login_wrong_password(client,user): assert client.post("/api/auth/login",json={"email":"user@example.com","password":"wrong"}).status_code==401
def test_public_events(client):
    r=client.get("/api/events"); assert r.status_code==200 and r.get_json()==[]
>>>>>>> 93f660917251956e4d1be85cd249fe95ff9b5fe6
