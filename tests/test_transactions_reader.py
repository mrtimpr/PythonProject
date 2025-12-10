from pathlib import Path
from typing import Any, Dict, List, Optional, cast
from unittest.mock import patch

import pandas as pd
import pytest

import src.transactions_reader as tr

Transaction = Dict[str, Any]


def _make_basic_df(extra_cols: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Утилита: создаёт DataFrame с обязательными колонками и опционально дополнительными."""
    data: Dict[str, Any] = {
        "transaction_id": [1, 2],
        "date": [pd.Timestamp("2020-01-01"), pd.Timestamp("2020-01-02")],
        "amount": [100.0, 200.0],
    }
    if extra_cols:
        data.update(extra_cols)
    return pd.DataFrame(data)


def _make_basic_transaction_list(extra_cols: Optional[Dict[str, Any]] = None) -> List[Transaction]:
    """Утилита: создаёт ожидаемый список словарей транзакций."""
    df = _make_basic_df(extra_cols)
    return cast(List[Transaction], df.to_dict(orient="records"))


def test__validate_df_raises_on_missing_columns() -> None:
    df: pd.DataFrame = pd.DataFrame({"transaction_id": [1], "date": [pd.Timestamp("2020-01-01")]})
    with pytest.raises(ValueError) as excinfo:
        tr._validate_df(df, ["transaction_id", "date", "amount"])
    assert "Missing columns:" in str(excinfo.value)
    assert "amount" in str(excinfo.value)


def test_read_transactions_csv_forwards_parse_dates_and_kwargs_and_returns_list_of_dicts() -> None:
    mock_df: pd.DataFrame = _make_basic_df()
    expected_result: List[Transaction] = _make_basic_transaction_list()

    with patch("src.transactions_reader.pd.read_csv", return_value=mock_df) as mock_read_csv:
        path: str = "transactions.csv"
        res: List[Transaction] = tr.read_transactions_csv(path, sep=";", encoding="utf-8")
        assert res == expected_result
        mock_read_csv.assert_called_once_with(path, parse_dates=["date"], sep=";", encoding="utf-8")


def test_read_transactions_csv_accepts_pathlib_path_and_custom_required_columns() -> None:
    mock_df: pd.DataFrame = _make_basic_df(extra_cols={"category": ["a", "b"]})
    expected_result: List[Transaction] = _make_basic_transaction_list(extra_cols={"category": ["a", "b"]})

    with patch("src.transactions_reader.pd.read_csv", return_value=mock_df) as mock_read_csv:
        p: Path = Path("some/path/transactions.csv")
        required_cols: List[str] = ["transaction_id", "date", "amount", "category"]

        res: List[Transaction] = tr.read_transactions_csv(p, required_columns=required_cols)

        assert res == expected_result

        mock_read_csv.assert_called_once_with(p, parse_dates=["date"])


def test_read_transactions_csv_raises_if_missing_columns_from_csv() -> None:
    df_no_amount: pd.DataFrame = pd.DataFrame({"transaction_id": [1], "date": [pd.Timestamp("2020-01-01")]})
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

        mock_read_excel.assert_called_once_with(path, sheet_name="Sheet1", parse_dates=["date"], engine="openpyxl")


def test_read_transactions_xlsx_default_sheet_and_missing_columns() -> None:
    bad_df: pd.DataFrame = pd.DataFrame({"date": [pd.Timestamp("2020-01-01")], "amount": [10.0]})
    with patch("src.transactions_reader.pd.read_excel", return_value=bad_df):
        with pytest.raises(ValueError):
            tr.read_transactions_xlsx("f.xlsx")
