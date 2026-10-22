import base64
import os
import secrets
from urllib.parse import urlencode, parse_qs, urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer

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

