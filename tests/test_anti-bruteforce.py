from tests.utils import extract_csrf

def test_login_message_generic_for_unknown_user(client):
    token = extract_csrf(client.get("/login").data)
    r = client.post("/login", data={
        "csrf_token": token,
        "email": "nouser@test.com",
        "password": "WrongPassword!123",
    }, follow_redirects=True)

    assert r.status_code == 200
    assert b"Identifiants invalides" in r.data
