import builtins
from typing import Any, Dict, List
from unittest.mock import Mock, patch

from main import (
    Transaction,
    display_results,
    get_user_status_choice,
    handle_sorting_choice,
    main,
    select_and_load_data,
    yes_no_prompt,
)


def test_yes_no_prompt_true_da(monkeypatch) -> None:
    monkeypatch.setattr(builtins, "input", lambda prompt="": "Да")
    assert yes_no_prompt("Вопрос") is True


def test_yes_no_prompt_true_d_short(monkeypatch) -> None:
    monkeypatch.setattr(builtins, "input", lambda prompt="": "д")
    assert yes_no_prompt("Вопрос") is True


def test_yes_no_prompt_false(monkeypatch) -> None:
    monkeypatch.setattr(builtins, "input", lambda prompt="": "нет")
    assert yes_no_prompt("Вопрос") is False


def test_handle_sorting_choice_no_prompt(monkeypatch) -> None:
    sample: List[Transaction] = [{"id": 1}]  # type: ignore[typeddict-item]
    monkeypatch.setattr("main.yes_no_prompt", lambda prompt: False)
    result = handle_sorting_choice(sample)
    assert result is sample


def test_handle_sorting_choice_yes_calls_sort_by_date_ascending(monkeypatch) -> None:
    sample: List[Transaction] = [{"id": 1}]  # type: ignore[typeddict-item]
    monkeypatch.setattr("main.yes_no_prompt", lambda prompt: True)
    monkeypatch.setattr(builtins, "input", lambda prompt="": "возрастанию")

    mock_sorted: List[Transaction] = [{"id": 1, "sorted": "asc"}]  # type: ignore[typeddict-item]
    mock_sort: Mock = Mock(return_value=mock_sorted)

    with patch("main.sort_by_date", mock_sort):
        result = handle_sorting_choice(sample)
        mock_sort.assert_called_once_with(sample, False)
        assert result is mock_sorted


def test_handle_sorting_choice_yes_calls_sort_by_date_desc_short(monkeypatch) -> None:
    sample: List[Transaction] = [{"id": 2}]  # type: ignore[typeddict-item]
    monkeypatch.setattr("main.yes_no_prompt", lambda prompt: True)
    monkeypatch.setattr(builtins, "input", lambda prompt="": "у")

    mock_sorted: List[Transaction] = [{"id": 2, "sorted": "desc"}]  # type: ignore[typeddict-item]
    mock_sort: Mock = Mock(return_value=mock_sorted)

    with patch("main.sort_by_date", mock_sort):
        result = handle_sorting_choice(sample)
        mock_sort.assert_called_once_with(sample, True)
        assert result is mock_sorted


def test_display_results_empty(capsys) -> None:
    display_results([])
    captured = capsys.readouterr()
    assert "Распечатываю итоговый список транзакций" in captured.out
    assert "Не найдено ни одной транзакции" in captured.out


def test_display_results_with_various_transactions(capsys) -> None:
    tx1: Transaction = {
        "date": "2020-01-01",
        "description": "Описание 1",
        "from": "account_from_1",
        "to": "account_to_1",
        "operationAmount": {"amount": "100.00", "currency": {"name": "RUB"}},
    }
    tx2: Dict[str, Any] = {
        "date": "2020-02-02",
        "description": "Описание 2",
        "to": "account_to_2",
        "amount": "50.5",
        "currency_code": "USD",
    }
    transactions: List[Any] = [tx1, tx2]

    with (
        patch("main.get_date", side_effect=lambda d: f"DATE[{d}]"),
        patch("main.mask_account_card", side_effect=lambda s: f"MASK[{s}]" if s else ""),
    ):
        display_results(transactions)
        out = capsys.readouterr().out

        # Базовая часть вывода
        assert "Распечатываю итоговый список транзакций" in out
        assert "Всего банковских операций в выборке: 2" in out

        # Новая встроенная статистика категорий
        assert "Описание 1: 1" in out
        assert "Описание 2: 1" in out

        # Проверка вывода транзакций
        assert "DATE[2020-01-01] Описание 1" in out
        assert "MASK[account_from_1] -> MASK[account_to_1]" in out
        assert "Сумма: 100.00 RUB" in out

        assert "DATE[2020-02-02] Описание 2" in out
        assert "MASK[account_to_2]" in out
        assert "-> MASK[account_to_2]" not in out
        assert "Сумма: 50.5 USD" in out


def test_display_results_handles_malformed_amounts(capsys) -> None:
    tx: Dict[str, Any] = {
        "date": "2020-03-03",
        "description": "Некорректная сумма",
        "to": "acct",
        "operationAmount": "not a dict",
    }

    with patch("main.get_date", return_value="DATE"), patch("main.mask_account_card", return_value="MASK[acct]"):
        display_results([tx])
        out = capsys.readouterr().out
        assert "DATE Некорректная сумма" in out
        assert "-> MASK[acct]" in out
        assert "Сумма: Неизвестно" in out


def test_main_returns_when_no_data(monkeypatch, capsys):
    monkeypatch.setattr("main.select_and_load_data", lambda: None)
    monkeypatch.setattr("main.get_user_status_choice", lambda *a, **k: None)
    main()
    out = capsys.readouterr().out
    assert "Привет! Добро пожаловать в программу" in out


def test_main_full_flow_filters_and_display(monkeypatch):
    import builtins
    from unittest.mock import Mock

    initial_data = [
        {"id": 1, "operationAmount": {"amount": "100", "currency": {"code": "RUB", "name": "RUB"}}},
        {"id": 2, "operationAmount": {"amount": "200", "currency": {"code": "USD", "name": "USD"}}},
    ]
    after_state = initial_data
    after_sort = initial_data
    after_currency = [{"id": 1, "operationAmount": {"amount": "100", "currency": {"code": "RUB", "name": "RUB"}}}]
    after_search = after_currency

    # Мокаем загрузчик данных
    monkeypatch.setattr("main.select_and_load_data", lambda: initial_data)

    # Мокаем выбор статуса
    monkeypatch.setattr("main.get_user_status_choice", lambda statuses: "EXECUTED")

    # Мокаем filter_by_state
    mock_filter_state = Mock(return_value=after_state)
    monkeypatch.setattr("main.filter_by_state", mock_filter_state)

    # Мокаем сортировку
    mock_handle_sort = Mock(return_value=after_sort)
    monkeypatch.setattr("main.handle_sorting_choice", mock_handle_sort)

    monkeypatch.setattr("main.yes_no_prompt", Mock(side_effect=[True, True]))

    # Мокаем ввод слова
    monkeypatch.setattr(builtins, "input", lambda prompt="": "оплата")

    # Мокаем поиск
    mock_search = Mock(return_value=after_search)
    monkeypatch.setattr("main.process_bank_search", mock_search)

    # Мокаем display_results
    mock_display = Mock()
    monkeypatch.setattr("main.display_results", mock_display)

    from main import main

    main()
    mock_filter_state.assert_called_once_with(initial_data, "EXECUTED")
    mock_handle_sort.assert_called_once_with(after_state)

    mock_search.assert_called_once_with(after_currency, "оплата")

    mock_display.assert_called_once_with(after_search)


def test_select_and_load_data_json_choice(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", lambda prompt="": "1")
    mock_loader = Mock(return_value=[{"id": 10}])
    with patch("main.load_transaction_data", mock_loader):
        data = select_and_load_data()
        out = capsys.readouterr().out
        assert data == [{"id": 10}]
        assert "Для обработки выбран файл" in out


def test_select_and_load_data_csv_choice(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", lambda prompt="": "2")
    mock_loader = Mock(return_value=[{"id": 20}])
    with patch("main.read_transactions_csv", mock_loader):
        data = select_and_load_data()
        out = capsys.readouterr().out
        assert data == [{"id": 20}]
        assert "Для обработки выбран файл" in out


def test_select_and_load_data_xlsx_choice(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", lambda prompt="": "3")
    mock_loader = Mock(return_value=[{"id": 30}])
    with patch("main.read_transactions_xlsx", mock_loader):
        data = select_and_load_data()
        out = capsys.readouterr().out
        assert data == [{"id": 30}]
        assert "Для обработки выбран файл" in out


def test_select_and_load_data_file_not_found(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", lambda prompt="": "2")

    def raise_fn(path):
        raise FileNotFoundError

    with patch("main.read_transactions_csv", side_effect=raise_fn):
        data = select_and_load_data()
        out = capsys.readouterr().out
        assert data is None
        assert "Ошибка: Файл" in out and "не найден" in out


def test_select_and_load_data_loader_exception(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", lambda prompt="": "3")

    def raise_val(path):
        raise ValueError("boom")

    with patch("main.read_transactions_xlsx", side_effect=raise_val):
        data = select_and_load_data()
        out = capsys.readouterr().out
        assert data is None
        assert "Ошибка при чтении файла" in out and "boom" in out


def test_select_and_load_data_invalid_choice(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", lambda prompt="": "999")
    data = select_and_load_data()
    out = capsys.readouterr().out
    assert data is None
    assert "Неверный ввод. Завершение программы." in out


def test_get_user_status_choice_valid_first_try(monkeypatch):
    """
    Пользователь вводит корректный статус сразу.
    """
    mock_input = Mock(return_value="executed")
    monkeypatch.setattr(builtins, "input", mock_input)

    result = get_user_status_choice({"EXECUTED", "CANCELED", "PENDING"})

    assert result == "EXECUTED"
    mock_input.assert_called_once()


def test_get_user_status_choice_invalid_then_valid(monkeypatch):
    """
    Пользователь сначала вводит неверный статус, затем корректный.
    Проверяем, что функция запрашивает повторно.
    """
    mock_input = Mock(side_effect=["wrong", "PENDING"])
    monkeypatch.setattr(builtins, "input", mock_input)

    result = get_user_status_choice({"EXECUTED", "CANCELED", "PENDING"})

    assert result == "PENDING"
    assert mock_input.call_count == 2


def test_get_user_status_choice_returns_uppercase(monkeypatch):
    """
    Функция должна приводить ввод пользователя к верхнему регистру.
    """
    mock_input = Mock(return_value="canceled")
    monkeypatch.setattr(builtins, "input", mock_input)

    result = get_user_status_choice({"EXECUTED", "CANCELED", "PENDING"})

    assert result == "CANCELED"
