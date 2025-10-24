import masks


def mask_account_card(users_data: str) -> str:
    """функция которая умеет обрабатывать информацию как о картах, так и о счетах.
    Возвращая строку с замаскированным номером."""
    if "Счет" in users_data:
        bank_number_account = users_data[-20:]
        return users_data[:-20] + masks.get_mask_account(bank_number_account)
    else:
        bank_card_number = users_data[-16:]
        return users_data[:-16] + masks.get_mask_card_number(bank_card_number)
