from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Union, cast

import pandas as pd

Transaction = Dict[str, Any]

REQUIRED_COLUMNS: Set[str] = {"id", "date", "amount"}


def _validate_df(df: pd.DataFrame, required: Iterable[str]) -> None:
    missing: Set[str] = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")


def read_transactions_csv(
    path: Union[str, Path], required_columns: Optional[Iterable[str]] = None, **kwargs: Any
) -> List[Transaction]:
    """
    Читает CSV-файл транзакций и возвращает список словарей.
    """
    cols_to_check: Iterable[str]
    if required_columns is None:
        cols_to_check = REQUIRED_COLUMNS
    else:
        cols_to_check = required_columns

    df: pd.DataFrame = pd.read_csv(path, parse_dates=["date"], sep=";", **kwargs)
    _validate_df(df, cols_to_check)

    raw_list_of_dicts = df.to_dict(orient="records")
    return cast(List[Transaction], raw_list_of_dicts)


def read_transactions_xlsx(
    path: Union[str, Path],
    sheet_name: Union[str, int] = 0,
    required_columns: Optional[Iterable[str]] = None,
    **kwargs: Any,
) -> List[Transaction]:
    """
    Читает XLSX-файл (Excel) транзакций и возвращает список словарей.
    """
    cols_to_check: Iterable[str]
    if required_columns is None:
        cols_to_check = REQUIRED_COLUMNS
    else:
        cols_to_check = required_columns

    df: pd.DataFrame = pd.read_excel(path, sheet_name=sheet_name, parse_dates=["date"], **kwargs)
    _validate_df(df, cols_to_check)

    raw_list_of_dicts = df.to_dict(orient="records")
    return cast(List[Transaction], raw_list_of_dicts)
