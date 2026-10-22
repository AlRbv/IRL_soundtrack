import base64

from app import auth


def test_build_auth_url_contains_state():
    url, state = auth.build_auth_url()
    assert url.startswith("https://accounts.spotify.com/authorize?")
    assert f"state={state}" in url


def test_get_tokens_sends_basic_auth(monkeypatch):
    captured = {}

    class FakeResp:
        ok = True

        def json(self):
            return {"access_token": "a"}

    def fake_post(url, headers, data):
        captured["headers"] = headers
        captured["data"] = data
        return FakeResp()

    monkeypatch.setattr(auth, "post", fake_post)

    assert auth.get_tokens_from_code("abc") == {"access_token": "a"}
    expected = base64.b64encode(f"{auth.CLIENT_ID}:{auth.CLIENT_SECRET}".encode()).decode()
    assert captured["headers"]["Authorization"] == "Basic " + expected
    assert captured["data"]["code"] == "abc"
