def test_session_cookie_flags_http_dev(client):
    r = client.get("/register")
    assert r.status_code == 200

    cookies = r.headers.getlist("Set-Cookie")
    if cookies:
        joined = " ".join(cookies).lower()
        assert "httponly" in joined
        assert "samesite" in joined
        assert "secure" not in joined
