import app.main
from app.main import main


def test_main_prints_status_ok(capsys, monkeypatch):
    monkeypatch.setattr(app.main, "get_access_token", lambda: "fake-token-123")
    assert main() == 0
    assert capsys.readouterr().out.strip().endswith("STATUS:OK")
