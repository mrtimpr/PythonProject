import pytest

from src.processing import filter_by_state, sort_by_date

from typing import Any


def test_filter_by_state_cn(list_dict: list, list_dict_filter: list) -> None:
    state: str = "CANCELED"
    assert filter_by_state(list_dict, state) == list_dict_filter


def test_filter_by_state_ex(list_dict: list, list_dict_filter_ex: list) -> None:
    state: str = "EXECUTED"
    assert filter_by_state(list_dict, state) == list_dict_filter_ex


@pytest.mark.parametrize(
    "n, expected_result",
    [
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            "Предоставленный ключ неверен",
        )
    ],
)
def test_filter_by_state_not_key(n: list, expected_result: list) -> None:
    state: str = ""
    assert filter_by_state(n, state) == expected_result


@pytest.mark.parametrize("n, expected_result", [("", "Проверьте что список словарей имеет данные")])
def test_filter_by_state_not_list(n: Any, expected_result: list) -> None:
    state: str = "EXECUTED"
    assert filter_by_state(n, state) == expected_result


def test_sort_by_date(list_dict: list, list_dict_sort: list) -> None:
    assert sort_by_date(list_dict) == list_dict_sort


def test_sort_by_date_invert(list_dict: list, list_dict_sort_invert: list) -> None:
    assert sort_by_date(list_dict, False) == list_dict_sort_invert


@pytest.mark.parametrize(
    "n, expected_result",
    [
        ("", "Проверьте что список словарей имеет данные"),
    ],
)
def test_sort_by_date_zero(n: Any, expected_result: list) -> None:
    assert sort_by_date(n) == expected_result
