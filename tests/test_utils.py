import json
import logging
from pathlib import Path
from unittest.mock import mock_open, patch

from src.utils import load_transaction_data

logging.basicConfig(level=logging.CRITICAL)


def normalize_path_separators(path_str: str) -> str:
    """Заменяет все разделители пути на стандартный слэш."""
    return path_str.replace("\\", "/")


def test_file_not_found() -> None:
    expected_path = Path("missing.json").resolve().as_posix()

    with patch("builtins.open", side_effect=FileNotFoundError("missing.json")):
        with patch("src.utils.logger.error") as mock_logger_error:
            result = load_transaction_data("missing.json")
            assert result == []
            mock_logger_error.assert_called_once()
            log_message = mock_logger_error.call_args.args[0]
            normalized_log_message = normalize_path_separators(log_message)
            assert "Ошибка: Файл не найден по пути" in normalized_log_message
            assert expected_path in normalized_log_message
            assert mock_logger_error.call_args.kwargs.get("exc_info") is True


def test_empty_file() -> None:
    m_open = mock_open(read_data="")
    with patch("builtins.open", m_open):
        with patch("src.utils.logger.warning") as mock_logger_warning:
            result = load_transaction_data("empty.json")
            assert result == []
            mock_logger_warning.assert_called_once_with("Файл empty.json пуст.")


def test_invalid_json() -> None:
    m_open = mock_open(read_data="not a json")
    with patch("builtins.open", m_open):
        with patch("src.utils.logger.error") as mock_logger_error:
            result = load_transaction_data("bad.json")
            assert result == []
            mock_logger_error.assert_called_once()
            assert "Ошибка декодирования JSON в файле bad.json:" in mock_logger_error.call_args.args[0]
            assert mock_logger_error.call_args.kwargs.get("exc_info") is True


def test_json_not_list() -> None:
    data = json.dumps({"a": 1})
    m_open = mock_open(read_data=data)
    with patch("builtins.open", m_open):
        with patch("src.utils.logger.error") as mock_logger_error:
            result = load_transaction_data("not_list.json")
            assert result == []
            expected_msg = "Ошибка: Содержимое файла not_list.json не является списком JSON. Получен тип: dict"
            mock_logger_error.assert_called_once_with(expected_msg)


def test_valid_json_list() -> None:
    data = json.dumps([{"id": 1, "amount": 100}])
    m_open = mock_open(read_data=data)
    with patch("builtins.open", m_open):
        with patch("src.utils.logger.info") as mock_logger_info:
            result = load_transaction_data("valid.json")
            assert result == [{"id": 1, "amount": 100}]
            mock_logger_info.assert_called()


def test_permission_denied_error() -> None:
    with patch("builtins.open", side_effect=PermissionError("Permission denied")):
        with patch("src.utils.logger.critical") as mock_logger_critical:
            result = load_transaction_data("secure.json")
            assert result == []
            mock_logger_critical.assert_called_once()
            log_message = mock_logger_critical.call_args.args[0]
            normalized_log_message = normalize_path_separators(log_message)

            assert normalized_log_message.startswith(
                normalize_path_separators("Произошла непредвиденная ошибка при чтении файла secure.json:")
            )
            assert "Permission denied" in normalized_log_message

            assert mock_logger_critical.call_args.kwargs.get("exc_info") is True


def test_empty_filepath_string() -> None:
    with patch("builtins.open", side_effect=FileNotFoundError):
        with patch("src.utils.logger.error") as mock_logger_error:
            result = load_transaction_data("")
            assert result == []
            mock_logger_error.assert_called()
            assert mock_logger_error.call_args.kwargs.get("exc_info") is True
