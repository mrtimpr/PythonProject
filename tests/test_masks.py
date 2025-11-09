from typing import Union

import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "n, expected_result",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        (7000792289606361, "7000 79** **** 6361"),
        ("", "Проверьте верность номера карты"),
        ("70007922896063619", "Проверьте верность номера карты"),
    ],
)
def test_get_mask_card_number(n: Union[str, int], expected_result: str) -> None:
    assert get_mask_card_number(n) == expected_result


@pytest.mark.parametrize(
    "n, expected_result",
    [
        ("73654108430135874305", "**4305"),
        (73654108430135874305, "**4305"),
        ("", "Проверьте верность номера счета"),
        ("70007922896063619", "Проверьте верность номера счета"),
    ],
)
def test_get_mask_account(n: Union[str, int], expected_result: str) -> None:
    assert get_mask_account(n) == expected_result
