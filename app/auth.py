import base64
import os
import json
import time
from pathlib import Path
import secrets
import webbrowser

from urllib.parse import urlencode, parse_qs, urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer

from dotenv import load_dotenv
from requests import post

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8888/callback"
TOKEN_PATH = Path(__file__).resolve().parent.parent / ".cache" / "spotify_token.json"
SCOPE = "user-library-read user-modify-playback-state playlist-read-private"

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

def clinet_headers() -> dict:
    auth_base64 = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode("utf-8")).decode("utf-8")
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded", 
    }
    return headers

def get_tokens_from_code(code: str) -> dict:
    headers = clinet_headers()
    data = {"grant_type": "authorization_code","code": code, "redirect_uri": REDIRECT_URI}

    result = post("https://accounts.spotify.com/api/token", headers=headers, data=data)

    if not result.ok:
        raise SystemExit(f"Token wasn't fecthed - {result.status_code} {result.text}")
    
    return result.json()


def wait_for_server_callback(expected_state: str, timeout: int = 20) -> str:
    result = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            query = parse_qs(urlparse(self.path).query)
            for key in ("code", "state", "error"):
                if key in query:
                    result[key] = query[key][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Login received. You can close the tab.")

        def log_message(self, format, *args):
            pass

    server = HTTPServer(("127.0.0.1", urlparse(REDIRECT_URI).port), Handler)

    server.timeout = timeout
    server.handle_request()
    server.server_close()

    if not result:
        raise SystemExit("Nothing sent from spotify. Timeout")
    if "error" in result: 
        raise SystemExit(f"Login failed {result["error"]}")
    if result.get("state") != expected_state:
        raise SystemExit("Failed to confirm user. Suspicious acitivity on login.")
    if "code" not in result:
        raise SystemExit("Redirect had no code. Try again")

    return result["code"]

def save_tokens(tokens: dict) -> dict:
    tokens = {**tokens, "expires_at": int(time.time()) + tokens["expires_in"]}
    TOKEN_PATH.parent.mkdir(exist_ok=True)
    TOKEN_PATH.write_text(json.dumps(tokens, indent=2), encoding="utf-8")
    TOKEN_PATH.chmod(0o600)
    return tokens

def load_tokens() -> dict | None:
    if not TOKEN_PATH.exists():
        return None
    try:
        return json.loads(TOKEN_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print(f"Token cache unreadable, ignoring: {TOKEN_PATH}")
        return None
    
def refresh_tokens(refresh_token: str) -> dict | None:
    data = {"grant_type": "refresh_token", "refresh_token": refresh_token}
    result = post("https://accounts.spotify.com/api/token", headers=clinet_headers(), data=data)

    if result.status_code == 400:
        print(f"Refresh token rejected, new login needed {result.text}")
        return None
    if not result.ok:
        raise SystemExit(f"Token refresh failed - {result.status_code} {result.text}")

    return {"refresh_token": refresh_token, **result.json()}

def has_all_scopes(tokens: dict) -> bool:
    required = set(SCOPE.split())
    granted = set(tokens.get("scope", "").split())
    return required <= granted

def get_access_token() -> str:
    tokens = load_tokens()

    if tokens and not has_all_scopes(tokens):
        print("Scopes needed changed, new loging needed")
        tokens = None

    if tokens and tokens["expires_at"] - 60 > time.time():
        return tokens["access_token"]

    if tokens and "refresh_token" in tokens:
        refreshed = refresh_tokens(tokens["refresh_token"])
        if refreshed:
            return save_tokens(refreshed)["access_token"]

    url, state = build_auth_url()
    print("Opening Spotify login in your browser...")
    webbrowser.open(url)
    code = wait_for_server_callback(state, timeout=120)
    return save_tokens(get_tokens_from_code(code))["access_token"]
