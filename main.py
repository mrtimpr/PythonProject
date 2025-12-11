import sys
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, TypedDict, cast

from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.transactions_reader import read_transactions_csv, read_transactions_xlsx
from src.utils import load_transaction_data
from src.utils_for_data import process_bank_search
from src.widget import get_date, mask_account_card

DATA_DIR = Path("data")
JSON_PATH = DATA_DIR / "operations.json"
CSV_PATH = DATA_DIR / "transactions.csv"
XLSX_PATH = DATA_DIR / "transactions_excel.xlsx"
AVAILABLE_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}


class CurrencyAmount(TypedDict):
    """Описание валюты и суммы вложенным словарем."""

    amount: str
    currency: Dict[Literal["name", "code"], str]


class Transaction(TypedDict, total=False):
    """Основной тип для представления банковской транзакции."""

    id: int
    state: str
    date: str
    operationAmount: CurrencyAmount
    amount: str  # Поле для CSV/XLSX структуры
    currency_code: str  # Поле для CSV/XLSX структуры
    description: str
    from_: str
    to: str


TransactionsList = List[Transaction]


def main() -> None:
    """Основная функция программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.\n")

    data: Optional[TransactionsList] = select_and_load_data()
    if data is None:
        return

    status = get_user_status_choice(AVAILABLE_STATUSES)
    filtered_data: TransactionsList = filter_by_state(cast(TransactionsList, data), status)

    if not filtered_data:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    filtered_data = handle_sorting_choice(filtered_data)

    if yes_no_prompt("\nВыводить только рублевые транзакции?"):
        filtered_data = list(filter_by_currency(filtered_data, "RUB"))

    if yes_no_prompt("\nОтфильтровать список транзакций по определенному слову в описании?"):
        word = input("Введите слово для фильтрации: ").strip()
        filtered_data = process_bank_search(filtered_data, word)

    display_results(filtered_data)


def select_and_load_data() -> Optional[TransactionsList]:
    """Запрашивает у пользователя выбор файла и загружает данные."""
    print("Выберите необходимый пункт меню:")
    print(f"1. Получить информацию о транзакциях из JSON-файла ({JSON_PATH})")
    print(f"2. Получить информацию о транзакциях из CSV-файла ({CSV_PATH})")
    print(f"3. Получить информацию о транзакциях из XLSX-файла ({XLSX_PATH})")

    file_choice = input().strip()

    file_map: Dict[str, tuple[Path, Any]] = {
        "1": (JSON_PATH, load_transaction_data),
        "2": (CSV_PATH, read_transactions_csv),
        "3": (XLSX_PATH, read_transactions_xlsx),
    }

    if file_choice in file_map:
        path, loader_func = file_map[file_choice]
        print(f"Для обработки выбран файл: {path}")
        try:
            data = loader_func(str(path))
            return data
        except FileNotFoundError:
            print(f"Ошибка: Файл '{path}' не найден.")
            return None
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return None
    else:
        print("Неверный ввод. Завершение программы.")
        return None


def get_user_status_choice(available_statuses: set[str]) -> str:
    """Запрашивает статус транзакции у пользователя."""
    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные статусы: {', '.join(sorted(available_statuses))}")
        status = input().strip().upper()
        if status in available_statuses:
            print(f'Операции отфильтрованы по статусу "{status}"')
            return status
        else:
            print(f'Статус операции "{status}" недоступен. Попробуйте снова.')


def yes_no_prompt(prompt_text: str) -> bool:
    """Универсальная функция для запросов Да/Нет."""
    user_input = input(f"{prompt_text} (Да/Нет)\n").strip().lower()
    return user_input in ("да", "д")


def handle_sorting_choice(filtered_data: TransactionsList) -> TransactionsList:
    """Обрабатывает выбор сортировки пользователем."""
    if yes_no_prompt("Отсортировать операции по дате?"):
        order_prompt = "Отсортировать по возрастанию или по убыванию? (возрастанию/убыванию)\n"
        order = input(order_prompt).strip().lower()

        # reverse=True означает сортировку по убыванию (от новых к старым)
        reverse = order in ("убыванию", "по убыванию", "у")

        return sort_by_date(cast(TransactionsList, filtered_data), reverse)
    return filtered_data


def display_results(transactions: TransactionsList) -> None:
    """Печатает итоговый список транзакций."""
    print("\nРаспечатываю итоговый список транзакций...\n")

    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(transactions)}\n")

    for tx in transactions:
        date = get_date(tx.get("date", ""))
        description = tx.get("description", "Описание отсутствует")
        from_masked = mask_account_card(tx.get("from_"))
        to_masked = mask_account_card(tx.get("to"))

        amount: str | Literal["Неизвестно"] = "Неизвестно"
        currency: str = ""

        if "operationAmount" in tx and tx["operationAmount"] is not None:
            try:
                op_amount: CurrencyAmount = tx["operationAmount"]
                amount = op_amount["amount"]
                currency = op_amount["currency"]["name"]
            except (KeyError, TypeError):
                pass
        elif "amount" in tx:
            amount = tx["amount"]
            currency = tx.get("currency_code", "")

        print(f"{date} {description}")

        if from_masked and to_masked:
            print(f"{from_masked} -> {to_masked}")
        elif to_masked:
            print(f"-> {to_masked}")

        print(f"Сумма: {amount} {currency}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма была прервана пользователем.")
        sys.exit(0)
