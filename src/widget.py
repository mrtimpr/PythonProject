from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(users_data: str) -> str:
    """функция которая умеет обрабатывать информацию как о картах, так и о счетах.
    Возвращая строку с замаскированным номером."""

    list_users_date = users_data.split()
    if len(list_users_date) == 0:
        return "Проверьте корректность предоставленных данных"
    else:
        if "Счет" in users_data:
            bank_number_account = list_users_date[-1]
            del list_users_date[-1]
            mask_account = get_mask_account(bank_number_account)
            if mask_account == "Проверьте верность номера счета":
                return "Проверьте верность номера счета"
            else:
                return " ".join(list_users_date) + " " + mask_account
        else:
            bank_card_number = list_users_date[-1]
            del list_users_date[-1]
            mask_card_number = get_mask_card_number(bank_card_number)
            if mask_card_number == "Проверьте верность номера карты":
                return "Проверьте верность номера карты"
            return " ".join(list_users_date) + " " + mask_card_number


def get_date(date_and_time: str) -> str:
    """функция, которая принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ" """
    try:
        read_date_and_time = datetime.strptime(date_and_time, "%Y-%m-%dT%H:%M:%S.%f")
        return datetime.strftime(read_date_and_time, "%d.%m.%Y")
    except ValueError:
        return "Проверьте верность указаной даты"
