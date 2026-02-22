import pytest

from src.decorators import log


def test_log_to_console_success(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def add(x: int, y: int) -> int:
        return x + y

    assert add(1, 2) == 3
    captured = capsys.readouterr()
    assert "add ok" in captured.out


def test_log_to_console_error(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def boom() -> None:
        raise ValueError("fail")

    with pytest.raises(ValueError):
        boom()

    captured = capsys.readouterr()
    assert "boom error: ValueError. Inputs:" in captured.out


def test_log_to_file_success(tmp_path) -> None:
    log_file = tmp_path / "mylog.txt"

    @log(filename=str(log_file))
    def add(x: int, y: int) -> int:
        return x + y

    assert add(1, 2) == 3
    text = log_file.read_text(encoding="utf-8")
    assert "add ok" in text


def test_log_to_file_error(tmp_path) -> None:
    log_file = tmp_path / "mylog.txt"

    @log(filename=str(log_file))
    def boom() -> None:
        raise RuntimeError("x")

    with pytest.raises(RuntimeError):
        boom()

    text = log_file.read_text(encoding="utf-8")
    assert "boom error: RuntimeError. Inputs:" in text
