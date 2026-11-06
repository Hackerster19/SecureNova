import os
from urllib.parse import urlencode

from flask import (
    Flask, redirect, url_for, session,
    request, render_template,abort
)

from dotenv import load_dotenv
from auth import configure_oauth, require_permission,validate_access_token

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
    APP_BASE_URL = os.getenv("APP_BASE_URL").rstrip("/")

    redirect_uri = f"{APP_BASE_URL}/callback"
    return oauth.auth0.authorize_redirect(
        redirect_uri,
        audience=os.getenv("AUTH0_AUDIENCE"),
        code_challenge_method="S256",
        prompt="login"
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

    if not user_info:
        abort(401)

    # Validate Auth0 access token
    access_token = token.get("access_token")
    

    try:
     access_token_payload = validate_access_token(access_token)
     print("TOKEN CLAIMS:", list(access_token_payload.keys()))
     print("USER PERMISSIONS:", access_token_payload.get("permissions", []))
    except Exception as e:
     print("TOKEN VALIDATION ERROR:", str(e))
     abort(401)

# Extract RBAC permissions
    user_info["permissions"] = access_token_payload.get("permissions", [])
    # Store authenticated user information
    session["user"] = dict(user_info)

    
    

    return redirect(url_for("dashboard"))
@app.route("/dashboard")
@require_permission("read:ai-data")
def dashboard():
    user = session.get("user")

    if not user:
        return redirect(url_for("login"))

    return render_template("dashboard.html", user=user)

@app.route("/logout")
def logout():
    session.clear()

    return_to = os.getenv("APP_BASE_URL").rstrip("/")

    logout_url = (
        f"https://{AUTH0_DOMAIN}/v2/logout?"
        + urlencode({
            "client_id": AUTH0_CLIENT_ID,
            "returnTo": return_to
        })
    )

    return redirect(logout_url)

@app.route("/chat", methods=["POST"])
def chat():
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return {"error": "Missing or invalid token"}, 401

    access_token = auth_header.split(" ", 1)[1]

    try:
        payload = validate_access_token(access_token)
    except Exception:
        return {"error": "Invalid or expired token"}, 401

    permissions = payload.get("permissions", [])

    if "read:ai-data" not in permissions:
        return {"error": "Insufficient permissions"}, 403

    return {
        "message": "Authenticated request successful",
        "agent_id": payload.get("https://securenova.ai/agent_id")
    }, 200

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=False
    )