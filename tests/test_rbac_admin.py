from sqlalchemy.orm import Session
from sqlalchemy import select

from tests.utils import extract_csrf
from app.webapp import User  # doit exister dans ton module


def _register_and_login(client, email="u@test.com", password="StrongPassword!123"):
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


def test_admin_denied_for_user(app, client):
    _register_and_login(client, "user1@test.com")
    r = client.get("/admin")
    assert r.status_code == 403


def test_admin_allowed_for_admin(app, client):
    email = "admin@test.com"
    _register_and_login(client, email)

    with app.app_context():
        with Session(app.engine) as s:
            u = s.scalar(select(User).where(User.email == email))
            u.role = "admin"
            s.commit()

    r = client.get("/admin")
    assert r.status_code == 200
