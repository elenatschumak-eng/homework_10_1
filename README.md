# SkyPro Python — Homework 11.1 (GitFlow + Processing + Generators + Tests)

This repository contains an educational Python project for practicing **Git/GitHub workflow (GitFlow)**, implementing **data processing utilities** (including **generators**), and writing **pytest** tests with **coverage reports**.

## Project goals

- Practice GitFlow workflow (`main`, `develop`, `feature/*`) and submit work via **Pull Requests** into `develop`.
- Implement reusable Python functions for filtering and sorting operation/transaction data.
- Implement generator-based utilities (`yield`) for efficient processing of transaction lists.
- Write tests using **pytest**, use fixtures/parametrization, and achieve **≥ 80%** test coverage.
- Keep code quality with **PEP 8**, **flake8**, and **mypy**.

## Requirements

- Python (recommended: the same version used in the course)
- Poetry

## Installation

1) Clone the repository:

```bash
git clone <REPO_URL>
cd <REPO_FOLDER>
```

2) Install dependencies:

```bash
poetry install
```

3) Activate the virtual environment (optional):

```bash
poetry shell
```

## Project structure

```text
src/
  processing.py    # filtering/sorting of operations
  generators.py    # generators for transaction processing (Homework 11.1)
  masks.py         # masking utilities (previous homework)
  widget.py        # widget functions (previous homework)

tests/
  test_processing.py
  test_masks.py
  test_widget.py
  test_generators.py

htmlcov/           # HTML coverage report (generated)
.coverage          # coverage data file (generated)
pyproject.toml
README.md
```

## Usage

### `filter_by_state` (module: `src/processing.py`)

Filters a list of operation dictionaries and returns only those operations whose `"state"` equals the provided state.
`state` is optional and defaults to `"EXECUTED"`.

```python
from src.processing import filter_by_state

ops = [
    {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 2, "state": "CANCELED", "date": "2018-06-30T02:08:58.425572"},
]

print(filter_by_state(ops))                # default state="EXECUTED"
print(filter_by_state(ops, "CANCELED"))    # explicit state
```

### `sort_by_date` (module: `src/processing.py`)

Sorts a list of operation dictionaries by `"date"` and returns a new sorted list.
`reverse` is optional and defaults to `True` (newest first).

```python
from src.processing import sort_by_date

ops = [
    {"id": 1, "date": "2019-07-03T18:35:29.512364"},
    {"id": 2, "date": "2018-06-30T02:08:58.425572"},
]

print(sort_by_date(ops))                 # descending by default
print(sort_by_date(ops, reverse=False))  # ascending
```

### `filter_by_currency` (module: `src/generators.py`)

Returns an iterator/generator that yields only transactions whose currency code matches the requested one (e.g., `"USD"`).

```python
from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")
print(next(usd_transactions))
print(next(usd_transactions))
```

### `transaction_descriptions` (module: `src/generators.py`)

Generator that yields each transaction `"description"` one by one.

```python
from src.generators import transaction_descriptions

descriptions = transaction_descriptions(transactions)
print(next(descriptions))
print(next(descriptions))
```

### `card_number_generator` (module: `src/generators.py`)

Generator that yields card numbers in the format `XXXX XXXX XXXX XXXX` for a given numeric range.

```python
from src.generators import card_number_generator

for card in card_number_generator(1, 5):
    print(card)
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
# 0000 0000 0000 0004
# 0000 0000 0000 0005
```

## Testing and quality checks

### Run tests

```bash
poetry run pytest
```

### Run flake8

```bash
poetry run flake8
```

### Run mypy

```bash
poetry run mypy src
```

### Run tests with coverage (terminal + HTML report)

```bash
poetry run pytest --cov=src --cov-report=term-missing --cov-report=html
```

After that, open the HTML report:

- Windows (PowerShell):
  ```powershell
  start htmlcov\index.html
  ```

## GitFlow workflow (short)

- `main`: stable branch
- `develop`: integration branch
- `feature/*`: development branches for each task

Work is done in a `feature/...` branch and then merged into `develop` via a Pull Request.
