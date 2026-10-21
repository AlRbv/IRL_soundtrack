from requests import post, get, put
import base64
import os
from dotenv import load_dotenv
import secrets
import webbrowser
from urllib.parse import urlencode, parse_qs, urlparse


load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "user-library-read user-modify-playback-state"

def build_auth_url():
    state = secrets.token_urlsafe(16)
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "state": state
    }
    url = "https://accounts.spotify.com/authorize?" + urlencode(params)
    return url, state

auth_url, state = build_auth_url()
print("Opening: ", auth_url)
webbrowser.open(auth_url)

redirect_comp = input("Please enter the redirect url from spotify: ").strip()

query = parse_qs(urlparse(redirect_comp).query)

if "error" in query:
    raise SystemExit("Spotify did not return a vaild URI")

returned_state = query["state"][0]
code = query["code"][0]

if returned_state != state:
    raise SystemExit("State mismatch. Suspiscious redirect. App stopped")

print("Code received:", code[:20] + "...")  

def get_tokens_from_code(code):
    auth_bytes = f"{CLIENT_ID}:{CLIENT_SECRET}".encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": "Basic " + auth_base64, 
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    result = post(url, headers=headers, data=data)

    if not result.ok:
        raise SystemExit(f"Token fetch failed. {result.status_code} {result.text}")

    return result.json()

tokens = get_tokens_from_code(code)  
access_token = tokens["access_token"]
refresh_token = tokens["refresh_token"]

print("access_token:", access_token[:10] + "...")
print("refresh_token:", refresh_token[:10] + "...")
print("expires:", tokens["expires_in"])
print("Scope:", tokens["scope"])


api_headers = {"Authorization": "Bearer " + access_token}

pause = put(
    "https://api.spotify.com/v1/me/player/pause",
    headers= api_headers
)

resp = get(
    "https://api.spotify.com/v1/me/tracks",  
    headers=api_headers,
    params={"limit": 50},             
)

if not resp.ok:
    raise SystemExit(f"song fetch failed. {resp.status_code} {resp.text}")

page = resp.json()

print(page["total"])

for i,item in enumerate(page["items"], start=1):    
    track = item["track"]
    print(f"{track["artists"][0]["name"]} - {track["name"]}")