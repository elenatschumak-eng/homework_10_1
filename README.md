# SkyPro Python — Homework 13.1 (CSV + XLSX Readers)

This repository is an educational Python project for practicing **Git/GitHub workflow (GitFlow)** and implementing small utilities for working with banking transactions.

The new functionality in this part (Homework 13.1) adds reading transactions from **CSV** and **Excel (XLSX)** files and returning them in a unified format: `list[dict]`.

---

## Project Goals

- Practice GitFlow workflow (`main`, `develop`, `feature/*`) and submitting work via Pull Requests into `develop`.
- Add readers for transaction data from **CSV** and **XLSX** files.
- Ensure stable behavior: on missing/empty/invalid files the readers return an empty list `[]` instead of crashing.
- Maintain code quality (PEP 8, docstrings, type hints) and run linters/tests.

---

## Requirements

- Python (course version)
- Poetry

Project dependencies are managed via Poetry and include:
- `pandas` (for CSV/XLSX parsing)
- `openpyxl` (Excel engine, used by pandas)

---

## Installation

~~~bash
git clone <REPO_URL>
cd <REPO_FOLDER>
poetry install
~~~

(Optional) Activate venv:
~~~bash
poetry shell
~~~

---

## Project Structure (relevant parts)

~~~text
data/
  operations.json
  transactions.csv
  transactions_excel.xlsx

src/
  data_readers.py      # Homework 13.1: CSV/XLSX readers
  utils.py             # JSON loader from previous homework parts
  processing.py        # filtering/sorting utilities
  generators.py        # generator utilities
  masks.py             # masking utilities
  widget.py            # widget utilities
  external_api.py      # currency conversion (API)

tests/
  test_data_readers.py
  ... other tests
~~~

---

## New Functionality (Homework 13.1): Reading CSV and Excel

### `read_transactions_csv(path)`

Reads transactions from a CSV file and returns `list[dict[str, Any]]`.

Key points:
- `path` is a filesystem path (string or `Path`)
- If the file is **missing**, **empty**, or cannot be parsed, the function returns `[]`
- In the provided dataset the separator is `;` (semicolon)

Example:
~~~python
from src.data_readers import read_transactions_csv

transactions = read_transactions_csv("data/transactions.csv")
print(len(transactions))
print(transactions[0])
~~~

---

### `read_transactions_excel(path, sheet_name=0)`

Reads transactions from an Excel `.xlsx` file and returns `list[dict[str, Any]]`.

Key points:
- `path` is a filesystem path (string or `Path`)
- `sheet_name` may be a sheet index (default `0`) or a sheet name
- If the file is **missing**, **empty**, or cannot be parsed, the function returns `[]`

Example:
~~~python
from src.data_readers import read_transactions_excel

transactions = read_transactions_excel("data/transactions_excel.xlsx")
print(len(transactions))
print(transactions[0])
~~~

---

## Running Tests and Linters

Run all tests:
~~~bash
poetry run pytest
~~~

Run coverage (optional):
~~~bash
poetry run pytest --cov=src --cov-report=term-missing --cov-report=html
~~~

Run flake8:
~~~bash
poetry run flake8
~~~

(Optional) Run mypy:
~~~bash
poetry run mypy src
~~~

---

## GitFlow (Short Overview)

- `main`: stable branch
- `develop`: integration branch
- `feature/*`: development branches for each homework part

Work is done in a `feature/...` branch and merged into `develop` via a Pull Request.