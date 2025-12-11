from typing import Any, Union


def filter_by_state(list_of_dicts: list[dict], state: str = "EXECUTED") -> Union[list[dict[Any, Any]], str]:
    """
    Функция filter_by_state, принимает список словарей и
    опционально значение для ключа state (по умолчанию 'EXECUTED').
    После работы функция возвращает новый список словарей,
    содержащий только те словари, у которых ключ state
    соответствует указанному значению.
    """
    if len(list_of_dicts) < 2:
        return "Проверьте что список словарей имеет данные"
    elif state != "EXECUTED" and state != "CANCELED" and state != "PENDING":
        return "Предоставленный ключ неверен"
    else:
        new_list_of_dicts = []
        for record in list_of_dicts:
            if record.get("state") == state:
                new_list_of_dicts.append(record)
        return new_list_of_dicts


def sort_by_date(list_of_dicts: list[dict], sort_parameter: bool = True) -> Union[list[dict[Any, Any]], str]:
    """
    Функция sort_by_date, принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание).
    """
    sorted_list = sorted(list_of_dicts, key=lambda tx: tx.get("date", ""), reverse=sort_parameter)
    return sorted_list
