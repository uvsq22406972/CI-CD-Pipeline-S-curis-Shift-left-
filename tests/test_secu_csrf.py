from tests.utils import extract_csrf

def test_register_get_has_csrf(client):
    r = client.get("/register")
    assert r.status_code == 200
    token = extract_csrf(r.data)
    assert token

def test_register_post_missing_csrf_is_400(client):
    r = client.post("/register", data={
        "email": "a@test.com",
        "password": "StrongPassword!123",
        "password2": "StrongPassword!123",
    })
    assert r.status_code == 400  # CSRF missing

def test_register_post_with_csrf_ok(client):
    r = client.get("/register")
    token = extract_csrf(r.data)

    r2 = client.post("/register", data={
        "csrf_token": token,
        "email": "a@test.com",
        "password": "StrongPassword!123",
        "password2": "StrongPassword!123",
    }, follow_redirects=True)

    assert r2.status_code == 200
