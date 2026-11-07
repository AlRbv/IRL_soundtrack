from requests import put

from app.auth import get_access_token

PAUSE_ENDPOINT = "https://api.spotify.com/v1/me/player/pause"

def pause_current_playback(token:str) -> None:
    url = PAUSE_ENDPOINT
    headers = {
        "Authorization": "Bearer " + token    
    }

    pause = put(url, headers=headers)

    if not pause.ok:
        raise SystemExit(f"Failed to pause_track: {pause.status_code} {pause.text}")

    print("Current track paused")

if __name__ == "__main__":
    pause_current_playback(get_access_token())