from tests.utils import extract_csrf, extract_csrf_anywhere

def _register(client, email="user@test.com", password="StrongPassword!123"):
    r = client.get("/register")
    token = extract_csrf(r.data)
    return client.post("/register", data={
        "csrf_token": token,
        "email": email,
        "password": password,
        "password2": password,
    }, follow_redirects=True)

def _login(client, email="user@test.com", password="StrongPassword!123"):
    r = client.get("/login")
    token = extract_csrf(r.data)
    return client.post("/login", data={
        "csrf_token": token,
        "email": email,
        "password": password,
    }, follow_redirects=True)

def test_full_auth_flow(client):
    r = _register(client)
    assert r.status_code == 200

    r2 = _login(client)
    assert r2.status_code == 200

    r3 = client.get("/dashboard")
    assert r3.status_code == 200

    #logout est POST + CSRF
    r4 = client.get("/dashboard")
    dash = client.get("/dashboard")
    token = extract_csrf_anywhere(dash.data)

    r5 = client.post("/logout", data={"csrf_token": token}, follow_redirects=True)
    assert r5.status_code == 200
