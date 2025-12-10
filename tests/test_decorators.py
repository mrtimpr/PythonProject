from pathlib import Path

import pytest

from src.decorators import log


def test_logs_success_to_file(tmp_path: Path) -> None:
    """При успешном выполнении функция должна писать лог в файл и возвращать результат."""
    logfile: Path = tmp_path / "test_log.txt"

    @log(str(logfile))
    def add(a: int, b: int) -> int:
        return a + b

    result: int = add(2, 3)
    assert result == 5

    text: str = logfile.read_text(encoding="utf-8")

    # проверки содержания лога
    assert "add ok" in text
    assert "Start:" in text
    assert "End:" in text
    assert "Duration:" in text
    assert "Result: 5" in text


def test_logs_success_to_stdout(capsys: pytest.CaptureFixture[str]) -> None:
    """При filename=None лог должен писаться в stdout."""

    @log()
    def greet(name: str) -> str:
        return f"Hello, {name}"

    res: str = greet("Alice")
    assert res == "Hello, Alice"

    captured = capsys.readouterr()
    out: str = captured.out

    assert "greet ok" in out
    assert "Start:" in out and "End:" in out and "Duration:" in out
    assert "Result: 'Hello, Alice'" in out


def test_logs_exception_and_reraises(tmp_path: Path) -> None:
    """Если функция выбрасывает исключение, декоратор должен залогировать ошибку и пробросить исходное исключение."""
    logfile = tmp_path / "err_log.txt"

    @log(str(logfile))
    def fail(x: int, y: int = 0) -> None:
        raise ValueError("boom")

    with pytest.raises(ValueError):
        fail(10, y=20)

    text: str = logfile.read_text(encoding="utf-8")

    # ожидаем сообщение об ошибке, имя исключения и упоминание входных аргументов
    assert "fail error" in text
    assert "ValueError" in text
    assert "Inputs:" in text
    assert "10" in text and "y=20" in text or "(10,)" in text


def test_log_timestamps_and_duration_format(tmp_path: Path) -> None:
    """Проверяем, что в логе есть метки времени и длительность не отрицательна."""
    logfile = tmp_path / "time_log.txt"

    @log(str(logfile))
    def quick() -> str:
        return "ok"

    quick()

    text: str = logfile.read_text(encoding="utf-8")
    # Проверяем наличие меток времени
    assert "Start:" in text and "End:" in text and "Duration:" in text
    assert "20" in text
