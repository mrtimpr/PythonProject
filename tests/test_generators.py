from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

"""Тесты по функции filter_by_currency"""


def test_filter_usd_currency(transactions: List[Dict[str, Any]]) -> None:
    """Проверка фильтрации по USD."""
    currency_to_filter = "USD"
    result = list(filter_by_currency(transactions, currency_to_filter))
    assert len(result) == 3
    assert result[0]["id"] == 939719570
    assert result[1]["id"] == 142264268
    assert result[2]["id"] == 895315941
    for transaction in result:
        code = transaction["operationAmount"]["currency"]["code"]
        assert code == currency_to_filter


def test_filter_rub_currency(transactions: List[Dict[str, Any]]) -> None:
    """Проверка фильтрации по RUB."""
    currency_to_filter = "RUB"
    result = list(filter_by_currency(transactions, currency_to_filter))
    assert len(result) == 2
    assert result[0]["id"] == 873106923
    assert result[1]["id"] == 594226727
    for transaction in result:
        code = transaction["operationAmount"]["currency"]["code"]
        assert code == currency_to_filter


def test_no_matching_currency(transactions: List[Dict[str, Any]]) -> None:
    """Проверка случая, когда совпадений по валюте нет."""
    result = list(filter_by_currency(transactions, "EUR"))
    assert len(result) == 0
    assert result == []


def test_invalid_input_type() -> None:
    """Проверка обработки некорректного типа входных данных (не список)."""
    with pytest.raises(TypeError, match="Ожидается список транзакций"):
        list(filter_by_currency("это не список", "USD"))  # type: ignore[arg-type]


"""Тесты по функции transaction_descriptions"""


def test_invalid_input_transaction_descriptions() -> None:
    """Проверка обработки некорректного типа входных данных (не список)."""
    with pytest.raises(TypeError, match="Ожидается список транзакций в качестве входных данных"):
        list(transaction_descriptions("это не список"))  # type: ignore[arg-type]


def test_transaction_descriptions(transactions: List[Dict[str, Any]]) -> None:
    """Проверка корректности вывода описаний."""
    descriptions: List[str] = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]
    assert list(transaction_descriptions(transactions)) == descriptions


"""Тесты по функции card_number_generator"""


@pytest.mark.parametrize(
    "start_meaning, end_meaning, expected_result",
    [(1, 2, ["0000 0000 0000 0001", "0000 0000 0000 0002"]), (1, 1, ["0000 0000 0000 0001"])],
)
def test_card_number_generator(start_meaning: int, end_meaning: int, expected_result: List[str]) -> None:
    assert list(card_number_generator(start_meaning, end_meaning)) == expected_result


def test_not_integers_card_number_generator() -> None:
    """Проверка обработки некорректного типа входных данных (не целые числа)."""
    with pytest.raises(TypeError, match="Начальное и конечное значения должны быть целыми числами."):
        list(card_number_generator("1", "1"))  # type: ignore[arg-type]


def test_invalid_input_card_number_generator() -> None:
    """Проверка обработки некорректных входных данных (стартовое больеш конечного)."""
    with pytest.raises(ValueError, match="Начальное значение не может быть больше конечного значения."):
        list(card_number_generator(2, 1))
