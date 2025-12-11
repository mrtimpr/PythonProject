import pytest

from src.processing import filter_by_state, sort_by_date


def test_filter_by_state_cn(list_dict: list, list_dict_filter: list) -> None:
    state: str = "CANCELED"
    assert filter_by_state(list_dict, state) == list_dict_filter


def test_filter_by_state_ex(list_dict: list, list_dict_filter_ex: list) -> None:
    state: str = "EXECUTED"
    assert filter_by_state(list_dict, state) == list_dict_filter_ex


@pytest.mark.parametrize(
    "state_key, expected_result",
    [
        ("INVALID", "Предоставленный ключ неверен"),
        ("", "Предоставленный ключ неверен"),
    ],
)
def test_filter_by_state_invalid_key(list_dict: list, state_key: str, expected_result: str) -> None:
    assert filter_by_state(list_dict, state_key) == expected_result


@pytest.mark.parametrize(
    "input_list, expected_result",
    [
        ([{"id": 1, "state": "EXECUTED"}], "Проверьте что список словарей имеет данные"),
        ([], "Проверьте что список словарей имеет данные"),
    ],
)
def test_filter_by_state_not_list(input_list: list, expected_result: str) -> None:
    state: str = "EXECUTED"
    assert filter_by_state(input_list, state) == expected_result


def test_sort_by_date(list_dict: list, list_dict_sort: list) -> None:
    assert sort_by_date(list_dict) == list_dict_sort


def test_sort_by_date_invert(list_dict: list, list_dict_sort_invert: list) -> None:
    assert sort_by_date(list_dict, False) == list_dict_sort_invert


def test_sort_by_date_empty_list() -> None:
    assert sort_by_date([]) == []
