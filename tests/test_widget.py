import math

import pandas as pd
import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "n, expected_result",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Visa Platinum 700079228960", "Проверьте верность номера карты"),
        ("", "Проверьте корректность предоставленных данных"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 7365410843013587430", "Проверьте верность номера счета"),
        (math.nan, ""),
        (73654108430135874305, "Проверьте верность номера карты"),
        ("Счет " + str(73654108430135874305), "Счет **4305"),
    ],
)
def test_mask_account_card(n: str | float | int, expected_result: str) -> None:

    if isinstance(n, float) and math.isnan(n):
        assert mask_account_card(pd.NA) == expected_result
    else:
        assert mask_account_card(n) == expected_result


@pytest.mark.parametrize(
    "n, expected_result",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("", "Проверьте верность указанной даты: недопустимый формат"),
        ("2024-13-11T02:26:18.671407", "Проверьте верность указанной даты: недопустимый формат"),
    ],
)
def test_get_date(n: str, expected_result: str) -> None:
    assert get_date(n) == expected_result
