import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    #Base de données en SQLite sur instance/
    DB_URL = os.environ.get("DB_URL", "sqlite:///instance/app.db")

    #Sessions/cookies sécurisés
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_SECURE = False

    #CSRF
    WTF_CSRF_TIME_LIMIT = 3600
