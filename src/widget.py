from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(users_data: str) -> str:
    """функция которая умеет обрабатывать информацию как о картах, так и о счетах.
    Возвращая строку с замаскированным номером."""
    if "Счет" in users_data:
        bank_number_account = users_data[-20:]
        return users_data[:-20] + get_mask_account(bank_number_account)
    else:
        bank_card_number = users_data[-16:]
        return users_data[:-16] + get_mask_card_number(bank_card_number)


def get_date(date_and_time: str) -> str:
    """функция, которая принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ" """
    received_date = date_and_time[8:10] + "." + date_and_time[5:7] + "." + date_and_time[:4]
    return received_date
