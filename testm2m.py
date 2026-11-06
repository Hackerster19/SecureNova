import os
import time
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("AUTH0_AGENT_CLIENT_ID")
CLIENT_SECRET = os.getenv("AUTH0_AGENT_CLIENT_SECRET")
AUDIENCE = os.getenv("AUTH0_AUDIENCE")

CHAT_URL = "http://127.0.0.1:5000/chat"


def timestamp():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


# Check that required environment variables exist
if not all([AUTH0_DOMAIN, CLIENT_ID, CLIENT_SECRET, AUDIENCE]):
    raise ValueError("Missing M2M configuration in .env")

# 1. Request an M2M access token
print(f"\n[{timestamp()}] Requesting M2M access token...")

token_response = requests.post(
    f"https://{AUTH0_DOMAIN}/oauth/token",
    json={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "audience": AUDIENCE,
        "grant_type": "client_credentials"
    },
    timeout=15
)

if token_response.status_code != 200:
    print("Token request failed:", token_response.status_code)
    print(token_response.text)
    raise SystemExit(1)

token_data = token_response.json()
access_token = token_data["access_token"]
expires_in = token_data.get("expires_in", 60)

print(f"[{timestamp()}] Token received. Expires in {expires_in} seconds.")

# 2. Call /chat using the valid token
print(f"\n[{timestamp()}] Sending request with valid token...")

headers = {"Authorization": f"Bearer {access_token}"}

valid_response = requests.post(
    CHAT_URL,
    headers=headers,
    timeout=15
)

print(f"[{timestamp()}] Valid token response: {valid_response.status_code}")
print(valid_response.text)

if valid_response.status_code != 200:
    print("Expected HTTP 200. Check the API permissions and token configuration.")
    raise SystemExit(1)

# 3. Wait until the token expires
wait_time = expires_in + 5

print(f"\n[{timestamp()}] Waiting {wait_time} seconds for token expiry...")
time.sleep(wait_time)

# 4. Replay the same token
print(f"\n[{timestamp()}] Replaying the expired token...")

expired_response = requests.post(
    CHAT_URL,
    headers=headers,
    timeout=15
)

print(f"[{timestamp()}] Expired token response: {expired_response.status_code}")
print(expired_response.text)

if expired_response.status_code == 401:
    print("\nSUCCESS: Expired token was rejected.")
else:
    print("\nExpected HTTP 401. Token expiry validation needs investigation.")