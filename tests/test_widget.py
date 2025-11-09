import pytest

from src.widget import mask_account_card, get_date


@pytest.mark.parametrize("n, expected_result", [
    ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
    ("Visa Platinum 700079228960", "Проверьте верность номера карты"),
    ("", "Проверьте корректность предоставленных данных"),
    ("Счет 73654108430135874305", "Счет **4305"),
    ("Счет 7365410843013587430", "Проверьте верность номера счета")])
def test_mask_account_card(n: str, expected_result: str) -> None:
    assert mask_account_card(n) == expected_result


@pytest.mark.parametrize("n, expected_result", [("Счет 73654108430135874305", "Счет **4305"), ("", "Проверьте верность номера счета"), ("70007922896063619", "Проверьте верность номера счета")])
def test_get_date(n: str, expected_result: str) -> None:
    assert get_date(n) == expected_result