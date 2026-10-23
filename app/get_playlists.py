from requests import get

from app.auth import get_access_token

PLAYLIST_ENDPOINT = "https://api.spotify.com/v1/me/playlists"

def fetch_saved_playlists(token: str) -> list[dict]:
    url = PLAYLIST_ENDPOINT
    params = {
        "limit": 50
    }
    headers = {
        "Authorization": "Bearer " + token    
    }
    playlists = []

    while url:
        resp = get(url, headers=headers, params=params)

        if not resp.ok:
            raise SystemExit(f"Failed to fetch playlists: {resp.status_code} {resp.text}")
  
        page = resp.json()
        playlists.extend(page["items"])

        url = page["next"]
        params = None

    return playlists

def print_fetched_playlists(playlists: list["dict"]) -> None:
    for i, playlist in enumerate(playlists, start = 1):
        print(f"{i:>3}. {playlist["name"]} owned by {playlist["owner"]["display_name"] if playlist["owner"]["display_name"] is not None else playlist["owner"]["id"]}. Songs: {playlist["items"]["total"]}")

if __name__ == "__main__":
    print_fetched_playlists(fetch_saved_playlists(get_access_token()))