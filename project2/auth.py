import os
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from functools import wraps
from flask import session, redirect, url_for, abort
import jwt
import requests
from functools import lru_cache

load_dotenv()

oauth = OAuth()

def configure_oauth(app):
    oauth.init_app(app)

    oauth.register(
        name="auth0",
        client_id=os.getenv("AUTH0_CLIENT_ID"),
        client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
        server_metadata_url=f"https://{os.getenv('AUTH0_DOMAIN')}/.well-known/openid-configuration",
        client_kwargs={
            "scope": "openid profile email read:ai-data write:admin"
        }
    )

    return oauth


def require_permission(permission):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = session.get("user")

            if not user:
                return redirect(url_for("login"))

            permissions = user.get("permissions", [])

            if permission not in permissions:
                abort(403)

            return func(*args, **kwargs)

        return wrapper
    return decorator


@lru_cache(maxsize=1)
def get_jwks():
    domain = os.getenv("AUTH0_DOMAIN")
    response = requests.get(
        f"https://{domain}/.well-known/jwks.json",
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def validate_access_token(token):
    domain = os.getenv("AUTH0_DOMAIN")
    audience = os.getenv("AUTH0_AUDIENCE")

    jwks = get_jwks()
    unverified_header = jwt.get_unverified_header(token)

    signing_key = None

    for key in jwks["keys"]:
        if key["kid"] == unverified_header.get("kid"):
            signing_key = jwt.algorithms.RSAAlgorithm.from_jwk(
                key
            )
            break

    if signing_key is None:
        raise jwt.InvalidTokenError("Signing key not found")

    payload = jwt.decode(
        token,
        signing_key,
        algorithms=["RS256"],
        audience=audience,
        issuer=f"https://{domain}/",
    )

    return payload