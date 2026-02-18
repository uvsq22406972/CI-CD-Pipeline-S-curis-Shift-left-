import os
import pytest

from app.webapp import create_app


@pytest.fixture()
def app(tmp_path, monkeypatch):
    # DB test dans un fichier temporaire
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("APP_ENV", "dev")
    monkeypatch.setenv("SECRET_KEY", "test-secret-key")
    monkeypatch.setenv("DB_URL", f"sqlite:///{db_path}")

    # HTTP-friendly
    monkeypatch.setenv("SESSION_COOKIE_SECURE", "false")
    monkeypatch.setenv("REMEMBER_COOKIE_SECURE", "false")
    monkeypatch.setenv("WTF_CSRF_SSL_STRICT", "false")

    # Evite flakiness rate-limit en tests (recommandé)
    monkeypatch.setenv("RATELIMIT_ENABLED", "false")

    app = create_app()
    app.config.update(TESTING=True)
    return app


@pytest.fixture()
def client(app):
    return app.test_client()
