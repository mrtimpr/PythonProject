import json
from unittest.mock import mock_open, patch

from src.utils import load_transaction_data


def test_file_not_found() -> None:
    with patch("src.utils.Path.exists", return_value=False):
        with patch("builtins.print") as mock_print:
            result = load_transaction_data("missing.json")
            assert result == []
            mock_print.assert_called_once_with("Ошибка: Файл не найден по пути missing.json")


def test_empty_file() -> None:
    with patch("src.utils.Path.exists", return_value=True):
        m_open = mock_open(read_data="")
        with patch("builtins.open", m_open):
            with patch("builtins.print") as mock_print:
                result = load_transaction_data("empty.json")
                assert result == []
                mock_print.assert_called_once_with("Ошибка: Файл empty.json пуст.")


def test_invalid_json() -> None:
    with patch("src.utils.Path.exists", return_value=True):
        m_open = mock_open(read_data="not a json")
        with patch("builtins.open", m_open):
            with patch("builtins.print") as mock_print:
                result = load_transaction_data("bad.json")
                assert result == []
                mock_print.assert_called_once_with("Ошибка: Не удалось декодировать JSON из файла bad.json.")


def test_json_not_list() -> None:
    with patch("src.utils.Path.exists", return_value=True):
        data = json.dumps({"a": 1})
        m_open = mock_open(read_data=data)
        with patch("builtins.open", m_open):
            with patch("builtins.print") as mock_print:
                result = load_transaction_data("not_list.json")
                assert result == []
                mock_print.assert_called_once_with("Ошибка: Содержимое файла not_list.json не является списком JSON.")


def test_valid_json_list() -> None:
    with patch("src.utils.Path.exists", return_value=True):
        data = json.dumps([{"id": 1, "amount": 100}])
        m_open = mock_open(read_data=data)
        with patch("builtins.open", m_open):
            # For a valid load we don't expect error prints; still safe to patch print to ensure no calls
            with patch("builtins.print") as mock_print:
                result = load_transaction_data("valid.json")
                assert result == [{"id": 1, "amount": 100}]
                mock_print.assert_not_called()


def test_unexpected_exception_during_open() -> None:
    with patch("src.utils.Path.exists", return_value=True):
        with patch("builtins.open", side_effect=PermissionError("denied")):
            with patch("builtins.print") as mock_print:
                result = load_transaction_data("perm.json")
                assert result == []
                mock_print.assert_called_once()
                called_arg = mock_print.call_args[0][0]
                assert called_arg.startswith("Произошла непредвиденная ошибка при чтении файла:")
