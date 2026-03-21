from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd  # type: ignore[import-untyped]


def _df_to_records(df: "pd.DataFrame") -> list[dict[str, Any]]:
    """
    Convert DataFrame to list of dicts and replace NaN with None.
    """
    df_clean = df.where(pd.notna(df), None)
    return [dict(r) for r in df_clean.to_dict(orient="records")]


def read_transactions_csv(path: str | Path) -> list[dict[str, Any]]:
    """
    Read transactions from a CSV file.

    Returns [] if the file is missing, empty, or cannot be parsed.
    """
    file_path = Path(path)

    if not file_path.exists() or not file_path.is_file():
        return []
    if file_path.stat().st_size == 0:
        return []

    try:
        df = pd.read_csv(file_path, sep=";")
    except (FileNotFoundError, OSError, ValueError, pd.errors.EmptyDataError):
        return []

    if df.empty:
        return []

    return _df_to_records(df)


def read_transactions_excel(path: str | Path, sheet_name: str | int = 0) -> list[dict[str, Any]]:
    """
    Read transactions from an Excel (XLSX) file.

    Returns [] if the file is missing, empty, or cannot be parsed.
    """
    file_path = Path(path)

    if not file_path.exists() or not file_path.is_file():
        return []
    if file_path.stat().st_size == 0:
        return []

    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    except (FileNotFoundError, OSError, ValueError):
        return []

    if isinstance(df, dict):
        return []

    if df.empty:
        return []

    return _df_to_records(df)
