def test_health(client):
    r=client.get("/health"); assert r.status_code==200 and r.get_json()["status"]=="ok"
def test_register_login(client):
    r=client.post("/api/auth/register",json={"username":"tester","email":"tester@example.com","password":"StrongPass123"}); assert r.status_code==201
    r=client.post("/api/auth/login",json={"email":"tester@example.com","password":"StrongPass123"}); assert r.status_code==200 and r.get_json()["token"]
def test_register_validation(client): assert client.post("/api/auth/register",json={"email":"bad@example.com"}).status_code==400
def test_login_wrong_password(client,user): assert client.post("/api/auth/login",json={"email":"user@example.com","password":"wrong"}).status_code==401
def test_public_events(client):
    r=client.get("/api/events"); assert r.status_code==200 and r.get_json()==[]
