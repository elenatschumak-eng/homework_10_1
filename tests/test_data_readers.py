from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

from src.data_readers import read_transactions_csv, read_transactions_excel


def test_read_transactions_csv_missing_file_returns_empty_list(tmp_path: Path) -> None:
    missing = tmp_path / "missing.csv"
    assert read_transactions_csv(missing) == []


def test_read_transactions_csv_empty_file_returns_empty_list(tmp_path: Path) -> None:
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("", encoding="utf-8")
    assert read_transactions_csv(empty_file) == []


@patch("src.data_readers.pd.read_csv")
def test_read_transactions_csv_ok_returns_records(mock_read_csv, tmp_path: Path) -> None:
    # File must exist and be non-empty, otherwise your function may return [] before calling pandas
    file_path = tmp_path / "transactions.csv"
    file_path.write_text("a;b\n1;2\n", encoding="utf-8")

    df = pd.DataFrame([{"id": 1, "amount": "10.00"}, {"id": 2, "amount": "20.00"}])
    mock_read_csv.return_value = df

    result = read_transactions_csv(file_path)

    assert result == [{"id": 1, "amount": "10.00"}, {"id": 2, "amount": "20.00"}]
    mock_read_csv.assert_called_once()
    # Optional streng: falls du sep=";" nutzt, lass diese Zeile drin.
    # Wenn deine Implementierung keinen sep setzt, sag mir kurz Bescheid, dann passe ich den Test an.
    assert mock_read_csv.call_args.kwargs.get("sep") in (";", None)


@patch("src.data_readers.pd.read_csv", side_effect=ValueError("bad csv"))
def test_read_transactions_csv_parse_error_returns_empty_list(mock_read_csv, tmp_path: Path) -> None:
    file_path = tmp_path / "bad.csv"
    file_path.write_text("not,a,csv", encoding="utf-8")

    assert read_transactions_csv(file_path) == []


def test_read_transactions_excel_missing_file_returns_empty_list(tmp_path: Path) -> None:
    missing = tmp_path / "missing.xlsx"
    assert read_transactions_excel(missing) == []


@patch("src.data_readers.pd.read_excel")
def test_read_transactions_excel_ok_returns_records(mock_read_excel, tmp_path: Path) -> None:
    # File must exist and be non-empty
    file_path = tmp_path / "transactions.xlsx"
    file_path.write_bytes(b"dummy")

    df = pd.DataFrame([{"id": 10, "amount": "99.99"}])
    mock_read_excel.return_value = df

    result = read_transactions_excel(file_path)

    assert result == [{"id": 10, "amount": "99.99"}]
    mock_read_excel.assert_called_once()


@patch("src.data_readers.pd.read_excel", side_effect=OSError("bad xlsx"))
def test_read_transactions_excel_error_returns_empty_list(mock_read_excel, tmp_path: Path) -> None:
    file_path = tmp_path / "bad.xlsx"
    file_path.write_bytes(b"dummy")

    assert read_transactions_excel(file_path) == []
