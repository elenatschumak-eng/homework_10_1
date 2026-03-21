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

---

## New Functionality (Homework 13.2): `re`, `collections.Counter`, and `main()`

In Homework 13.2 the project is extended with:
- Searching transactions by a substring in the `description` field using **regular expressions** (`re`)
- Counting how many transactions match each requested category using **`collections.Counter`**
- A `main()` entry point that connects the functionality and provides a simple CLI flow

### Search in descriptions with `re`

Module: `src/search_and_stats.py`  
Function: `process_bank_search(data, search)`

What it does:
- Takes a list of transaction dictionaries (`data`) and a search string (`search`)
- Uses `re` to find transactions where the `description` contains the search text (case-insensitive)
- Returns a list of matching transactions
- If `search` is empty, returns an empty list `[]`

Example:
~~~python
from src.search_and_stats import process_bank_search

ops = [
    {"id": 1, "description": "Перевод со счета на счет"},
    {"id": 2, "description": "Открытие вклада"},
]
print(process_bank_search(ops, "вклад"))
# -> [{"id": 2, "description": "Открытие вклада"}]
~~~

---

### Count categories with `collections.Counter`

Module: `src/search_and_stats.py`  
Function: `process_bank_operations(data, categories)`

What it does:
- Takes a list of transaction dictionaries (`data`) and a list of category strings (`categories`)
- Looks for each category as a substring match in `description` (case-insensitive)
- Uses `Counter` to calculate counts
- Returns a dictionary in the format `{category: count}`
- If `categories` is empty, returns `{}`

Example:
~~~python
from src.search_and_stats import process_bank_operations

ops = [
    {"description": "Перевод со счета на счет"},
    {"description": "Перевод с карты на карту"},
    {"description": "Открытие вклада"},
]
categories = ["Перевод", "вклад", "Кредит"]
print(process_bank_operations(ops, categories))
# -> {"Перевод": 2, "вклад": 1, "Кредит": 0}
~~~

---

### Program entry point (`main.py`)

The `main()` function is implemented in `main.py` (project root).  
It connects the modules and provides a user-facing workflow:
- Choose the data source (JSON / CSV / XLSX)
- Filter by operation status
- Optional sorting (ascending/descending)
- Optional RUB-only conversion
- Optional search by description and category statistics

Run the program:
~~~bash
poetry run python main.py
~~~
