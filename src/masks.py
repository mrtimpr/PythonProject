import logging
from typing import Union

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="masks.log",  # Запись логов в файл
    filemode="w",
)  # Перезапись файла при каждом запуске


get_get_mask_card_number = logging.getLogger("get_mask_card_number")
get_mask_account_logger = logging.getLogger("get_mask_account")

get_get_mask_card_number.setLevel(logging.DEBUG)
get_mask_account_logger.setLevel(logging.DEBUG)


def get_mask_card_number(bank_card_number: Union[str, int]) -> str:
    """Принимает на вход номер карты и возвращает ее маску в формате XXXX XX** **** XXXX , где X — это цифра номера."""
    get_get_mask_card_number.debug("Вызвана функция с входным типом: %s", type(bank_card_number).__name__)

    bank_card_number = str(bank_card_number)
    if len(bank_card_number) == 16:
        mask_card_number = bank_card_number[:4] + " " + bank_card_number[4:6] + "** **** " + bank_card_number[-4:]
        get_get_mask_card_number.info(
            f"Успешно сгенерирована маска для карты. Номер оканчивается на: {bank_card_number[-4:]}"
        )
        return mask_card_number
    else:
        error_message = f"Ошибка: Неверная длина номера карты ({len(bank_card_number)} символов, ожидалось 16)."
        get_get_mask_card_number.error(error_message)
        return "Проверьте верность номера карты"


def get_mask_account(bank_number_account: Union[str, int]) -> str:
    """принимает на вход номер счета и возвращает его маску в формате **XXXX , где X— это цифра номера."""
    get_mask_account_logger.debug("Вызвана функция с входным типом: %s", type(bank_number_account).__name__)
    bank_number_account = str(bank_number_account)
    if len(bank_number_account) == 20:
        mask_account = "**" + bank_number_account[-4:]
        get_mask_account_logger.info(
            f"Успешно сгенерирована маска для счета. Номер оканчивается на: {bank_number_account[-4:]}"
        )
        return mask_account
    else:
        error_message = f"Ошибка: Неверная длина номера счета ({len(bank_number_account)} символов, ожидалось 20)."
        get_mask_account_logger.error(error_message)
        return "Проверьте верность номера счета"
