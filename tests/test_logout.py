def test_logout_get_not_allowed(client):
    r = client.get("/logout")
    assert r.status_code in (405, 404)
