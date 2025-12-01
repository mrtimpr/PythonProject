import json
from unittest.mock import mock_open, patch

from src.utils import load_transaction_data


def test_file_not_found() -> None:
    with patch("builtins.open", side_effect=FileNotFoundError("missing.json")):
        with patch("builtins.print") as mock_print:
            result = load_transaction_data("missing.json")
            assert result == []
            # Проверяем, что сообщение об ошибке корректно выведено
            mock_print.assert_called_once_with("Ошибка: Файл не найден по пути missing.json")


def test_empty_file() -> None:
    m_open = mock_open(read_data="")
    with patch("builtins.open", m_open):
        with patch("builtins.print") as mock_print:
            result = load_transaction_data("empty.json")
            assert result == []
            mock_print.assert_called_once_with("Ошибка: Файл empty.json пуст.")


def test_invalid_json() -> None:
    m_open = mock_open(read_data="not a json")
    with patch("builtins.open", m_open):
        with patch("builtins.print") as mock_print:
            result = load_transaction_data("bad.json")
            assert result == []
            mock_print.assert_called_once_with("Ошибка: Не удалось декодировать JSON из файла bad.json.")


def test_json_not_list() -> None:
    data = json.dumps({"a": 1})
    m_open = mock_open(read_data=data)
    with patch("builtins.open", m_open):
        with patch("builtins.print") as mock_print:
            result = load_transaction_data("not_list.json")
            assert result == []
            mock_print.assert_called_once_with("Ошибка: Содержимое файла not_list.json не является списком JSON.")


def test_valid_json_list() -> None:
    data = json.dumps([{"id": 1, "amount": 100}])
    m_open = mock_open(read_data=data)
    with patch("builtins.open", m_open):
        with patch("builtins.print") as mock_print:
            result = load_transaction_data("valid.json")
            assert result == [{"id": 1, "amount": 100}]
            mock_print.assert_not_called()


def test_permission_denied_error() -> None:
    with patch("builtins.open", side_effect=PermissionError("Permission denied")):
        with patch("builtins.print") as mock_print:
            result = load_transaction_data("secure.json")
            assert result == []
            mock_print.assert_called_once()
            called_arg = mock_print.call_args[0][0]
            assert called_arg.startswith("Произошла непредвиденная ошибка при чтении файла:")
            assert "Permission denied" in called_arg


def test_empty_filepath_string() -> None:
    with patch("builtins.open", side_effect=FileNotFoundError):
        with patch("builtins.print") as mock_print:
            result = load_transaction_data("")
            assert result == []
            assert mock_print.called
