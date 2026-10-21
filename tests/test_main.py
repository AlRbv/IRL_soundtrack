from app.main import main


def test_main_prints_status_ok(capsys):
    assert main() == 0
    assert capsys.readouterr().out.strip().endswith("STATUS:OK")
