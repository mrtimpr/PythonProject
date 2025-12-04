from typing import Any
from unittest.mock import Mock, patch

import requests
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

import src.external_api
from src.external_api import convert_to_rub

src.external_api.HTTPError = HTTPError  # type: ignore[misc]
src.external_api.ConnectionError = ConnectionError  # type: ignore[misc]
src.external_api.Timeout = Timeout  # type: ignore[misc]
src.external_api.RequestException = RequestException  # type: ignore[misc]

src.external_api.API_KEY = "test-api-key"  # type: ignore[misc]


def test_convert_when_currency_rub_returns_amount_and_does_not_call_api() -> None:
    tx = {"operationAmount": {"amount": "150.50", "currency": {"code": "RUB"}}}

    with patch("requests.get") as mock_get:
        result = convert_to_rub(tx)
        assert result == 150.50
        mock_get.assert_not_called()


@patch("requests.get")
def test_convert_successful_api_conversion(mock_get: Mock) -> None:
    # Подготовим мок-ответ от requests.get
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {"result": 987.65}
    mock_get.return_value = mock_response

    tx = {"operationAmount": {"amount": "10", "currency": {"code": "USD"}}}

    result = convert_to_rub(tx)

    assert result == 987.65
    # Проверим, что requests.get вызван с ожидаемым URL и заголовком
    expected_url = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=10.0"
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert expected_url in args[0]
    assert kwargs["headers"] == {"apikey": "test-api-key"}
    assert "timeout" in kwargs and kwargs["timeout"] == 5


@patch("requests.get")
def test_api_returns_unexpected_format_returns_zero_and_prints_error(mock_get: Mock, capsys: Any) -> None:
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {"unexpected": 1}
    mock_get.return_value = mock_response

    tx = {"operationAmount": {"amount": "5", "currency": {"code": "EUR"}}}

    result = convert_to_rub(tx)
    assert result == 0.0

    captured = capsys.readouterr()
    assert "Ошибка API" in captured.out


def test_invalid_input_keyerror_returns_zero(capsys: Any) -> None:
    # Отсутствует ключ operationAmount -> KeyError внутри функции
    tx = {"bad": "data"}
    result = convert_to_rub(tx)
    assert result == 0.0
    captured = capsys.readouterr()
    assert "Ошибка обработки входных данных" in captured.out


@patch("requests.get")
def test_http_error_from_raise_for_status_returns_zero(mock_get: Mock, capsys: Any) -> None:
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("HTTP failure")
    mock_get.return_value = mock_response

    tx = {"operationAmount": {"amount": "1", "currency": {"code": "GBP"}}}

    result = convert_to_rub(tx)
    assert result == 0.0
    captured = capsys.readouterr()
    assert "Ошибка HTTP запроса" in captured.out


@patch("requests.get")
def test_connection_error_on_get_returns_zero(mock_get: Mock, capsys: Any) -> None:
    mock_get.side_effect = requests.exceptions.ConnectionError("Connection lost")

    tx = {"operationAmount": {"amount": "2", "currency": {"code": "AUD"}}}

    result = convert_to_rub(tx)
    assert result == 0.0
    captured = capsys.readouterr()
    assert "Ошибка подключения к сети" in captured.out


@patch("requests.get")
def test_timeout_on_get_returns_zero(mock_get: Mock, capsys: Any) -> None:
    mock_get.side_effect = requests.exceptions.Timeout("timeout")

    tx = {"operationAmount": {"amount": "3", "currency": {"code": "CAD"}}}

    result = convert_to_rub(tx)
    assert result == 0.0
    captured = capsys.readouterr()
    assert "Превышено время ожидания ответа от API" in captured.out


@patch("requests.get")
def test_request_exception_on_get_returns_zero(mock_get: Mock, capsys: Any) -> None:
    mock_get.side_effect = requests.exceptions.RequestException("other error")

    tx = {"operationAmount": {"amount": "4", "currency": {"code": "NZD"}}}

    result = convert_to_rub(tx)
    assert result == 0.0
    captured = capsys.readouterr()
    assert "Неизвестная ошибка запроса" in captured.out


def test_value_error_in_amount_returns_zero(capsys: Any) -> None:
    tx = {"operationAmount": {"amount": "not_a_number", "currency": {"code": "USD"}}}

    result = convert_to_rub(tx)
    assert result == 0.0
    captured = capsys.readouterr()
    assert "Ошибка обработки входных данных" in captured.out
