"""
Page de connexion/inscription sécurisé en Flask.

Structure inspirée de (code entièrement réécrit et adapté en Python/Flask):
https://medium.com/@ajuatahcodingarena/building-a-secure-login-and-registration-system-with-html-css-javascript-php-and-mysql-591f839ee8f3

Améliorations de sécurité ajoutées:
- Protection CSRF sur les formulaires
- Hachage sur les mots de passe avec bcrypt
- Limitation du nombre de tentatives (anti brute-force)
- Entêtes HTTP de sécurité
- Validation des entrées utilisateur
- Accès au base de données sécurisé via SQLAlchemy
"""

import re
from datetime import timedelta

from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_wtf.csrf import CSRFProtect

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
    UserMixin,
)

from werkzeug.security import generate_password_hash, check_password_hash

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask_talisman import Talisman

from sqlalchemy import create_engine, String, Integer, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

from config import Config
from flask import request  # en haut du fichier



# =========================
# Définition de la base SQL
# =========================

class Base(DeclarativeBase):
    """Classe de base SQLAlchemy."""
    pass


class User(Base, UserMixin):
    """
    Modèle utilisateur minimal: id, email unique, mot de passe haché.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

#Création du moteur de base de données
engine = create_engine(Config.DB_URL, future=True)


def init_db():
    """Création des tables si elles n'existent pas."""
    Base.metadata.create_all(engine)


# =========================
# Définition des formulaires
# =========================

class LoginForm(FlaskForm):
    """Formulaire de connexion avec validation."""
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=8, max=128)])


class RegisterForm(FlaskForm):
    """Formulaire d'inscription avec confirmation du mot de passe."""
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Email requis."),
            Email(message="Email invalide."),
            Length(max=255, message="Email trop long.")
        ],
    )
    password = PasswordField(
        "Mot de passe",
        validators=[
            DataRequired(message="Mot de passe requis."),
            Length(min=12, max=128, message="Mot de passe trop court (12 caractères minimum).")
        ],
    )
    password2 = PasswordField(
        "Confirmation du mot de passe",
        validators=[
            DataRequired(message="Confirmation requise."),
            EqualTo("password", message="Les mots de passe ne correspondent pas.")
        ],
    )



# =========================
# Création de l'application
# =========================

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    csrf = CSRFProtect()
    csrf.init_app(app)

    #Durée de vie de session
    app.permanent_session_lifetime = timedelta(hours=8)

    #Ajout d'entêtes de sécurité HTTP (CSP, etc.)
    Talisman(
        app,
        content_security_policy={"default-src": ["'self'"], "style-src": ["'self'"]},
        force_https=False,
    )

    #Limitation du nombre de requêtes par IP (anti brute-force)
    limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

    #Gestionnaire d'authentification Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        """Charge l'utilisateur depuis la base à partir de son ID."""
        try:
            uid = int(user_id)
        except ValueError:
            return None

        with Session(engine) as s:
            return s.get(User, uid)

    # Initialisation de la base
    init_db()

    # =========================
    # Fonction de vérification du mot de passe
    # =========================
    def mot_de_passe_robuste(pw: str) -> bool:
        """
        Vérifie la robustesse minimale : >= 12 caractères, minuscule, majuscule, chiffre, caractère spécial
        """
        if len(pw) < 12:
            return False

        return (
            re.search(r"[a-z]", pw)
            and re.search(r"[A-Z]", pw)
            and re.search(r"\d", pw)
            and re.search(r"[^A-Za-z0-9]", pw)
        )

    # =========================
    # Routes web
    # =========================

    @app.get("/")
    def index():
        """Page d'accueil."""
        return render_template("index.html")

    # ---------- INSCRIPTION ----------
    @app.route("/register", methods=["GET", "POST"])
    @limiter.limit("10 per hour")
    def register():
        """Création d'un nouveau compte utilisateur."""
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))

        form = RegisterForm()

        if form.validate_on_submit():
            email = form.email.data.strip().lower()
            password = form.password.data

            #Vérification robustesse
            if not mot_de_passe_robuste(password):
                flash("Mot de passe trop faible : 12+ caractères, majuscule, minuscule, chiffre, caractère spécial.", "warning")
                return render_template("register.html", form=form)

            pw_hash = generate_password_hash(password)

            with Session(engine) as s:
                #Vérifie si email déjà existant
                if s.scalar(select(User).where(User.email == email)):
                    flash("Email déjà utilisé.", "warning")
                    return render_template("register.html", form=form)

                s.add(User(email=email, password_hash=pw_hash))
                s.commit()

            flash("Compte créé avec succès.", "success")
            return redirect(url_for("login"))
        if request.method == "POST" and not form.validate():
            flash("Formulaire invalide — corrige les champs en rouge.", "danger")
            print("ERREURS REGISTER:", form.errors)
        return render_template("register.html", form=form)

    # ---------- CONNEXION ----------
    @app.route("/login", methods=["GET", "POST"])
    @limiter.limit("10 per minute")
    def login():
        """Connexion utilisateur sécurisée."""
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))

        form = LoginForm()

        if form.validate_on_submit():
            email = form.email.data.strip().lower()
            password = form.password.data

            with Session(engine) as s:
                user = s.scalar(select(User).where(User.email == email))

            #Message générique pour éviter l’énumération d’utilisateurs
            if not user or not check_password_hash(user.password_hash, password):
                flash("Identifiants invalides.", "danger")
                return render_template("login.html", form=form)

            login_user(user)
            flash("Connexion réussie.", "success")
            return redirect(url_for("dashboard"))

        return render_template("login.html", form=form)

    # ---------- DASHBOARD ----------
    @app.get("/dashboard")
    @login_required
    def dashboard():
        """Page protégée accessible uniquement après authentification."""
        return render_template("dashboard.html", email=current_user.email)

    # ---------- DÉCONNEXION ----------
    @app.post("/logout")
    @login_required
    def logout():
        """Déconnexion sécurisée (POST + CSRF)."""
        logout_user()
        flash("Déconnecté.", "info")
        return redirect(url_for("index"))

    return app


#Lancement direct en mode développement
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
