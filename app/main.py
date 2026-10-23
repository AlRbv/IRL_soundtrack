import sys

from app.auth import get_access_token
from app.get_saved import print_fetched_tracks, fetch_saved_tracks
from app.get_playlists import print_fetched_playlists, fetch_saved_playlists


def main() -> int:
    try:
        token = get_access_token()
    except SystemExit as e:
        print(e, file=sys.stderr)
        print("STATUS:AUTH_FAILED")
        return 1
    print("access_token:", token[:10] + "...")
    print("STATUS:OK")
    return 0

print_fetched_tracks(fetch_saved_tracks(get_access_token()))

print_fetched_playlists(fetch_saved_playlists(get_access_token()))

if __name__ == "__main__":
    sys.exit(main())
