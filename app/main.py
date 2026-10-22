import sys

from app.auth import get_access_token


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


if __name__ == "__main__":
    sys.exit(main())
