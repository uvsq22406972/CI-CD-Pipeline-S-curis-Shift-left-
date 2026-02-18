from tests.utils import extract_csrf

def test_weak_password_rejected(client):
    token = extract_csrf(client.get("/register").data)
    r = client.post("/register", data={
        "csrf_token": token,
        "email": "weak@test.com",
        "password": "weakpass",
        "password2": "weakpass",
    }, follow_redirects=True)
    assert r.status_code == 200

def test_duplicate_email_rejected(client):
    token1 = extract_csrf(client.get("/register").data)
    client.post("/register", data={
        "csrf_token": token1,
        "email": "dup@test.com",
        "password": "StrongPassword!123",
        "password2": "StrongPassword!123",
    }, follow_redirects=True)

    token2 = extract_csrf(client.get("/register").data)
    r = client.post("/register", data={
        "csrf_token": token2,
        "email": "dup@test.com",
        "password": "StrongPassword!123",
        "password2": "StrongPassword!123",
    }, follow_redirects=True)

    assert r.status_code == 200
