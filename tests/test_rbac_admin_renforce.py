def test_admin_redirects_if_not_logged(client):
    r = client.get("/admin", follow_redirects=False)
    assert r.status_code in (302, 401)
