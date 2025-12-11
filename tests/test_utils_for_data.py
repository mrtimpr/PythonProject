import re
from unittest.mock import Mock, patch

from src.utils_for_data import process_bank_operations, process_bank_search


def test_process_bank_search_empty_search() -> None:
    data = [{"id": 1, "description": "Оплата услуг"}]
    assert process_bank_search(data, "") == []


def test_process_bank_search_case_insensitive_and_non_string() -> None:
    data = [
        {"id": 1, "description": "Оплата услуг мобильной связи"},
        {"id": 2, "description": None},
        {"id": 3, "description": 123},
        {"id": 4, "description": "Оплата услуг интернета"},
    ]
    result = process_bank_search(data, "оплата")
    assert isinstance(result, list)
    assert [item["id"] for item in result] == [1, 4]


def test_process_bank_search_regex_escaping() -> None:
    data = [{"id": 1, "description": "special[chars].*+?"}]
    result = process_bank_search(data, "special[chars].*+?")
    assert [item["id"] for item in result] == [1]


def test_process_bank_search_patch_re_compile() -> None:
    data = [
        {"id": 1, "description": "match me"},
        {"id": 2, "description": "nope"},
    ]
    search = "match"

    mock_pattern = Mock()
    mock_pattern.search = Mock(side_effect=lambda s: "match" in s.lower())

    with patch("src.utils_for_data.re.compile", return_value=mock_pattern) as mock_compile:
        result = process_bank_search(data, search)

        mock_compile.assert_called_once_with(re.escape(search), re.IGNORECASE)

        assert [item["id"] for item in result] == [1]


def test_process_bank_operations_basic_counts() -> None:
    data = [
        {"id": 1, "description": "Оплата услуг мобильной связи"},
        {"id": 2, "description": "Покупка в магазине электроники"},
        {"id": 3, "description": "Перевод на карту: зарплата"},
        {"id": 4, "description": "Оплата услуг интернета"},
    ]
    categories = ["оплата", "покупка", "зарплата"]
    counts = process_bank_operations(data, categories)
    assert counts == {"оплата": 2, "покупка": 1, "зарплата": 1}


def test_process_bank_operations_overlapping_and_non_string() -> None:
    data = [
        {"description": "pay and payment both appear"},
        {"description": "payment only"},
        {"description": 123},
    ]
    categories = ["pay", "payment"]
    counts = process_bank_operations(data, categories)

    assert counts == {"pay": 2, "payment": 2}


def test_process_bank_operations_empty_categories() -> None:
    data = [{"description": "anything"}]
    assert process_bank_operations(data, []) == {}


def test_process_bank_operations_patch_compile() -> None:
    data = [
        {"description": "has_a"},
        {"description": "has_b"},
        {"description": "has_none"},
    ]
    categories = ["a", "b"]

    pat_a = Mock()
    pat_a.search = Mock(side_effect=lambda s: "a" in s)
    pat_b = Mock()
    pat_b.search = Mock(side_effect=lambda s: "b" in s)

    with patch("src.utils_for_data.re.compile", side_effect=[pat_a, pat_b]) as mock_compile:
        counts = process_bank_operations(data, categories)

        assert mock_compile.call_count == 2
        assert mock_compile.call_args_list[0][0] == (re.escape("a"), re.IGNORECASE)
        assert mock_compile.call_args_list[1][0] == (re.escape("b"), re.IGNORECASE)
        assert counts == {"a": 3, "b": 1}
