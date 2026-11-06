import os
from urllib.parse import urlencode

from flask import (
    Flask, redirect, url_for, session,
    request, render_template_string
)

from dotenv import load_dotenv
from auth import configure_oauth

load_dotenv()

# Initialize Flask
app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY")

if not app.secret_key:
    raise RuntimeError("FLASK_SECRET_KEY is missing from .env")

# Session security
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=True
)

# Connect Auth0
oauth = configure_oauth(app)

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")


@app.route("/")
def home():
    return """
    <h1>SecureNova AI</h1>
    <p>AI Chat Service with Auth0 Identity Security</p>
    <a href="/login">Login with Auth0</a>
    """


@app.route("/login")
def login():
    redirect_uri = url_for("callback", _external=True)

    return oauth.auth0.authorize_redirect(
        redirect_uri,
        code_challenge_method="S256"
    )


@app.route("/callback")
def callback():
    token = oauth.auth0.authorize_access_token()

    user_info = token.get("userinfo")

    if not user_info:
        user_info = oauth.auth0.parse_id_token(
            token,
            nonce=session.get("auth0_nonce")
        )

    session["user"] = dict(user_info)

    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    user = session.get("user")

    if not user:
        return redirect(url_for("login"))

    return render_template_string("""
        <h1>Welcome to SecureNova!</h1>
        <p>Authenticated successfully through Auth0.</p>
        <p>User: {{ user.get('name', 'User') }}</p>
        <p>Email: {{ user.get('email', 'Not available') }}</p>
        <a href="/logout">Logout</a>
    """, user=user)


@app.route("/logout")
def logout():
    session.clear()

    return_to = request.url_root.rstrip("/")

    logout_url = (
        f"https://{AUTH0_DOMAIN}/v2/logout?"
        + urlencode({
            "client_id": AUTH0_CLIENT_ID,
            "returnTo": return_to
        })
    )

    return redirect(logout_url)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=False
    )