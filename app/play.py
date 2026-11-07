from requests import put

from app.auth import get_access_token

PLAY_ENDPOINT = "https://api.spotify.com/v1/me/player/play"

def resume_current_playback(token:str) -> None:
    url = PLAY_ENDPOINT
    headers = {
        "Authorization": "Bearer " + token
    }

    play = put(url, headers=headers)

    if not play.ok:
        raise SystemExit(f"Failed to resume_track: {play.status_code} {play.text}")

    print("Current track resumed")

if __name__ == "__main__":
    resume_current_playback(get_access_token())
