from tests.utils import extract_csrf

def _register_and_login(client, email="u2@test.com", password="StrongPassword!123"):
    t = extract_csrf(client.get("/register").data)
    client.post("/register", data={
        "csrf_token": t,
        "email": email,
        "password": password,
        "password2": password,
    }, follow_redirects=True)

    t2 = extract_csrf(client.get("/login").data)
    client.post("/login", data={
        "csrf_token": t2,
        "email": email,
        "password": password,
    }, follow_redirects=True)

def test_logout_post_without_csrf_is_400(client):
    _register_and_login(client)
    r = client.post("/logout", data={}, follow_redirects=False)
    assert r.status_code == 400
