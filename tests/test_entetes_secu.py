def test_security_headers_present(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "X-Content-Type-Options" in r.headers
    assert "X-Frame-Options" in r.headers or "Content-Security-Policy" in r.headers
