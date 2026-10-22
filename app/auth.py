import base64
import os
import secrets
from urllib.parse import urlencode

from dotenv import load_dotenv
from requests import post

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "user-library-read user-modify-playback-state"

if not CLIENT_ID or not CLIENT_SECRET:
    raise SystemExit("client id/secret not found in .env")

def build_auth_url() -> tuple[str, str]:
    state = secrets.token_urlsafe(16)
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "state": state,
    }
    return "https://accounts.spotify.com/authorize?" + urlencode(params), state

def get_tokens_from_code(code: str) -> dict:
    auth_base64 = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode("utf-8")).decode("utf-8")
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded", 
    }
    data = {"grant_type": "authorization_code","code": code, "redirect_uri": REDIRECT_URI}

    result = post("https://accounts.spotify.com/api/token", headers=headers, data=data)

    if not result.ok:
        raise SystemExit(f"Token wasn't fecthed - {result.status_code} {result.text}")
    
    return result.json()
