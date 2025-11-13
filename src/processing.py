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
    elif state != "EXECUTED" and state != "CANCELED":
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
    if len(list_of_dicts) >= 1:
        sorted_list = sorted(list_of_dicts, key=lambda list_of_dicts: list_of_dicts["date"], reverse=sort_parameter)
        return sorted_list
    else:
        return "Проверьте что список словарей имеет данные"


print(
    sort_by_date(
        [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        ],
        False,
    )
)
