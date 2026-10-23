from requests import get

from app.auth import get_access_token

PLAYLIST_ENDPOINT = "https://api.spotify.com/v1/me/tracks"