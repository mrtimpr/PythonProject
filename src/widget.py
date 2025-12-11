import pandas as pd

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(users_data: str) -> str:
    """функция которая умеет обрабатывать информацию как о картах, так и о счетах.
    Возвращая строку с замаскированным номером."""

    if not isinstance(users_data, str):
        # Также можно явно проверить на float/NaN, которые приходят из pandas
        if pd.isna(users_data):
            return ""
        # Если это не строка, но не NaN, приведем к строке (например, если это int)
        users_data = str(users_data)

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
    """
    Функция, использующая pandas для гибкого парсинга даты и времени
    и возврата строки в формате "ДД.ММ.ГГГГ".
    """
    try:
        dt_object = pd.to_datetime(date_and_time)

        if pd.isna(dt_object):
            return "Проверьте верность указанной даты: недопустимый формат"

        return dt_object.strftime("%d.%m.%Y")

    except (ValueError, TypeError):
        return "Проверьте верность указанной даты: недопустимый формат"

    except Exception as e:
        return f"Произошла ошибка: {e}"
