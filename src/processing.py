def filter_by_state(list_of_dicts: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Функция filter_by_state, принимает список словарей и
    опционально значение для ключа state (по умолчанию 'EXECUTED').
    После работы функция возвращает новый список словарей,
    содержащий только те словари, у которых ключ state
    соответствует указанному значению.
    """

    new_list_of_dicts = []
    for list in list_of_dicts:
        if list.get("state") == state:
            new_list_of_dicts.append(list)
    return new_list_of_dicts


def sort_by_date(list_of_dicts: list[dict], sort_parameter: bool = True) -> list[dict]:
    """
    Функция sort_by_date, принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание).
    """
    sorted_list = sorted(list_of_dicts, key=lambda list_of_dicts: list_of_dicts["date"], reverse=sort_parameter)
    return sorted_list
