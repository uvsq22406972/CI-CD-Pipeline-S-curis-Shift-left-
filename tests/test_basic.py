from app.webapp import create_app


def test_homepage():
    app = create_app()
    client = app.test_client()

    response = client.get("/")
    assert response.status_code == 200
