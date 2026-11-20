from requests import get

from app.auth import get_access_token
from PIL import Image
from io import BytesIO

ALBUM_ENDPOINT = "https://api.spotify.com/v1/albums/"
TRACK_ENDPOINT = "https://api.spotify.com/v1/me/player/currently-playing"

def fetch_current_track_art(token: str) -> dict: 
    url = TRACK_ENDPOINT
    headers = {"Authorization": "Bearer " + token}

    resp = get(url, headers=headers)

    if not resp.ok:
            raise SystemExit(f"Failed to fetch tracks: {resp.status_code} {resp.text}")

    if resp.status_code == 204:
        print("Nothing is playing right now.")
        return None
    
    track = resp.json()

    images = track["item"]["album"]["images"]

    if not images:
        raise SystemExit(f"No image for the track: {track['item']['name']}")
    return images

def print_image(img: Image.Image, size: int = 32, aspect: float = 1.15) -> None:
    img = img.convert("RGB")

    side = min(img.width, img.height)
    left = (img.width - side) // 2
    top = (img.height - side) // 2
    img = img.crop((left, top, left + side, top + side))

    size += size % 2
    width = round(size * aspect)
    img = img.resize((width, size), Image.Resampling.BOX)
    px = img.load()

    for y in range(0, size, 2):
        line = ""
        for x in range(width):
            r1, g1, b1 = px[x, y]
            r2, g2, b2 = px[x, y + 1]
            line += f"\033[38;2;{r1};{g1};{b1}m\033[48;2;{r2};{g2};{b2}m▀"
        print(line + "\033[0m")   

def main() -> None:
    images = fetch_current_track_art(get_access_token())
    if images is None:
        return

    url = fetch_current_track_art(get_access_token())[0]["url"]      
    img = Image.open(BytesIO(get(url).content))
    print_image(img)

if __name__ == "__main__":
    main()

