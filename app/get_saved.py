'''
This one is purely for testing the fetched tokens. 
It pulls the saved tracks with the arstist and release date

Feel free to use as a sanity check after the tests are finished
'''

from requests import get

from app.auth import get_access_token

SAVED_ENDPOINT = "https://api.spotify.com/v1/me/tracks"


def fetch_saved_tracks(token: str) -> list[dict]:
    url = SAVED_ENDPOINT
    params = {"limit": 50}
    headers = {"Authorization": "Bearer " + token}

    resp = get(url, headers = headers, params=params)

    if not resp.ok:
        raise SystemExit(f"Failed to fetch tracks: {resp.status_code} {resp.text}")

    tracks = resp.json()["items"]

    return tracks


def print_fetched_tracks(tracks) -> None:

    for i, item in enumerate(tracks, start=1):
        track = item["track"]
        if track is None:
            continue
        print(f"{i:>3}. {track["artists"][0]["name"]} - {track["name"]} ({track["album"]["release_date"]})")

if __name__ == "__main__":
    print_fetched_tracks(fetch_saved_tracks(get_access_token()))