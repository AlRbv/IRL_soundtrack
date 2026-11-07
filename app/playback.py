import sys

from requests import post

from app.auth import get_access_token

NEXT_ENDPOINT = "https://api.spotify.com/v1/me/player/next"
PREVIOUS_ENDPOINT = "https://api.spotify.com/v1/me/player/previous"

def skip_to_next(token:str) -> None:
    url = NEXT_ENDPOINT
    headers = {
        "Authorization": "Bearer " + token
    }

    skip = post(url, headers=headers)

    if not skip.ok:
        raise SystemExit(f"Failed to skip_to_next: {skip.status_code} {skip.text}")

    print("Skipped to next track")

def skip_to_previous(token:str) -> None:
    url = PREVIOUS_ENDPOINT
    headers = {
        "Authorization": "Bearer " + token
    }

    skip = post(url, headers=headers)

    if not skip.ok:
        raise SystemExit(f"Failed to skip_to_previous: {skip.status_code} {skip.text}")

    print("Skipped to previous track")

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("next", "previous"):
        raise SystemExit("Usage: python -m app.playback next|previous")

    if sys.argv[1] == "next":
        skip_to_next(get_access_token())
    else:
        skip_to_previous(get_access_token())
