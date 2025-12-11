from pathlib import Path
from typing import Any, Dict, List, Optional, cast
from unittest.mock import patch

import pandas as pd
import pytest

import src.transactions_reader as tr

Transaction = Dict[str, Any]

# Новые имена колонок для соответствия обновленному коду
ID_COL = "id"
DATE_COL = "date"
AMOUNT_COL = "amount"


def _make_basic_df(extra_cols: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Утилита: создаёт DataFrame с обязательными колонками и опционально дополнительными."""
    data: Dict[str, Any] = {
        ID_COL: [1, 2],
        DATE_COL: [pd.Timestamp("2020-01-01"), pd.Timestamp("2020-01-02")],
        AMOUNT_COL: [100.0, 200.0],
    }
    if extra_cols:
        data.update(extra_cols)
    return pd.DataFrame(data)


def _make_basic_transaction_list(extra_cols: Optional[Dict[str, Any]] = None) -> List[Transaction]:
    """Утилита: создаёт ожидаемый список словарей транзакций."""
    df = _make_basic_df(extra_cols)
    return cast(List[Transaction], df.to_dict(orient="records"))


def test__validate_df_raises_on_missing_columns() -> None:
    df: pd.DataFrame = pd.DataFrame({ID_COL: [1], DATE_COL: [pd.Timestamp("2020-01-01")]})
    with pytest.raises(ValueError) as excinfo:
        tr._validate_df(df, [ID_COL, DATE_COL, AMOUNT_COL])
    assert "Missing columns:" in str(excinfo.value)
    assert AMOUNT_COL in str(excinfo.value)


def test_read_transactions_csv_forwards_parse_dates_and_kwargs_and_returns_list_of_dicts() -> None:
    mock_df: pd.DataFrame = _make_basic_df()
    expected_result: List[Transaction] = _make_basic_transaction_list()

    with patch("src.transactions_reader.pd.read_csv", return_value=mock_df) as mock_read_csv:
        path: str = "transactions.csv"
        res: List[Transaction] = tr.read_transactions_csv(path, encoding="utf-8")
        assert res == expected_result
        mock_read_csv.assert_called_once_with(path, parse_dates=[DATE_COL], sep=";", encoding="utf-8")


def test_read_transactions_csv_accepts_pathlib_path_and_custom_required_columns() -> None:
    extra_cols = {"category": ["a", "b"]}
    mock_df: pd.DataFrame = _make_basic_df(extra_cols=extra_cols)
    expected_result: List[Transaction] = _make_basic_transaction_list(extra_cols=extra_cols)

    with patch("src.transactions_reader.pd.read_csv", return_value=mock_df) as mock_read_csv:
        p: Path = Path("some/path/transactions.csv")
        required_cols: List[str] = [ID_COL, DATE_COL, AMOUNT_COL, "category"]

        res: List[Transaction] = tr.read_transactions_csv(p, required_columns=required_cols)

        assert res == expected_result

        mock_read_csv.assert_called_once_with(p, parse_dates=[DATE_COL], sep=";")


def test_read_transactions_csv_raises_if_missing_columns_from_csv() -> None:
    df_no_amount: pd.DataFrame = pd.DataFrame({ID_COL: [1], DATE_COL: [pd.Timestamp("2020-01-01")]})
    with patch("src.transactions_reader.pd.read_csv", return_value=df_no_amount):
        with pytest.raises(ValueError):
            tr.read_transactions_csv("f.csv")


def test_read_transactions_xlsx_forwards_args_and_returns_list_of_dicts() -> None:
    mock_df: pd.DataFrame = _make_basic_df()
    expected_result: List[Transaction] = _make_basic_transaction_list()

    with patch("src.transactions_reader.pd.read_excel", return_value=mock_df) as mock_read_excel:
        path: str = "transactions.xlsx"
        res: List[Transaction] = tr.read_transactions_xlsx(path, sheet_name="Sheet1", engine="openpyxl")
        assert res == expected_result

        mock_read_excel.assert_called_once_with(path, sheet_name="Sheet1", parse_dates=[DATE_COL], engine="openpyxl")


def test_read_transactions_xlsx_default_sheet_and_missing_columns() -> None:
    bad_df: pd.DataFrame = pd.DataFrame({DATE_COL: [pd.Timestamp("2020-01-01")], AMOUNT_COL: [10.0]})
    with patch("src.transactions_reader.pd.read_excel", return_value=bad_df):
        with pytest.raises(ValueError):
            tr.read_transactions_xlsx("f.xlsx")
