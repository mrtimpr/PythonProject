from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует список транзакций по указанному коду валюты.
    Поддерживает оба формата:
    - JSON (operationAmount.currency.code) (ранее поддерживал только его)
    - CSV/XLSX (currency_code)
    """
    if not isinstance(transactions, list):
        raise TypeError("Ожидается список транзакций в качестве входных данных")

    for record in transactions:
        try:
            # JSON-структура
            code_json = record.get("operationAmount", {}).get("currency", {}).get("code")

            # CSV/XLSX-структура
            code_csv = record.get("currency_code")

            if code_json == currency or code_csv == currency:
                yield record

        except AttributeError:
            print(f"Предупреждение: Некорректный формат записи транзакции: {record}")
            continue


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, который принимает список транзакций и возвращает итератор
    с описанием (description) каждой операции по очереди.
    """
    if not isinstance(transactions, list):
        raise TypeError("Ожидается список транзакций в качестве входных данных")
    for record in transactions:
        description = record.get("description")
        if description:
            yield description


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор, который выдает номера банковских карт в заданном диапазоне
    от start до end в формате XXXX XXXX XXXX XXXX.
    """
    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("Начальное и конечное значения должны быть целыми числами.")
    if start > end:
        raise ValueError("Начальное значение не может быть больше конечного значения.")
    len_card_num = 16
    for card_num_int in range(start, end + 1):
        card_num_str = f"{card_num_int:0{len_card_num}d}"
        formatted_card = " ".join([card_num_str[i : i + 4] for i in range(0, len_card_num, 4)])
        yield formatted_card
