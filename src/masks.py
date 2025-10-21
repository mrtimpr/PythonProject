from typing import Union


def get_mask_card_number(bank_card_number: Union[str, int]) -> str:
    """Принимает на вход номер карты и возвращает ее маску в формате XXXX XX** **** XXXX , где X — это цифра номера."""
    bank_card_number = str(bank_card_number)
    mask_card_number = bank_card_number[:4] + " " + bank_card_number[4:6] + "** **** " + bank_card_number[-4:]
    return mask_card_number


def get_mask_account(bank_number_account: Union[str, int]) -> str:
    """принимает на вход номер счета и возвращает его маску в формате **XXXX , где X— это цифра номера."""
    bank_number_account = str(bank_number_account)
    mask_account = "**" + bank_number_account[-4:]
    return mask_account
