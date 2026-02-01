# SkyPro Python – Homework 10.1 (GitFlow + Processing)

This repository contains a small educational project for practicing **Git/GitHub workflow (GitFlow)** and basic **data processing functions** in Python.
The project is focused on working with a list of banking operations represented as dictionaries.

## Project Goal

* Practice working with **Git branches** (`main`, `develop`, `feature/*`) and submitting work via **Pull Requests** into `develop`.
* Implement reusable Python functions for filtering and sorting operation data.
* Follow basic code quality rules (PEP 8, type hints, docstrings) and use linters/tests.

---

## Requirements

* Python (recommended: the same version used in the course)
* Poetry

---

## Installation

1. Clone the repository:

```bash
git clone <REPO_URL>
cd <REPO_FOLDER>
```

2. Install dependencies with Poetry:

```bash
poetry install
```

3. Activate the virtual environment (optional):

```bash
poetry shell
```

---

## Project Structure

```
src/
  processing.py   # data processing functions
  masks.py        # masking utilities (from previous homework)
  widget.py       # widget functions (from previous homework)

tests/
  ...             # tests (if provided / created)
```

---

## Usage

### `filter_by_state`

Filters a list of operation dictionaries and returns only those operations whose `"state"` equals the provided state.

* Parameter `state` is optional and defaults to `"EXECUTED"`.
* Input is a list of dictionaries (operations).

Example:

```python
from src.processing import filter_by_state

ops = [
    {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

print(filter_by_state(ops))
# -> only operations with state "EXECUTED"

print(filter_by_state(ops, "CANCELED"))
# -> only operations with state "CANCELED"
```

---

### `sort_by_date`

Sorts a list of operation dictionaries by the `"date"` field and returns a new sorted list.

* Parameter `reverse` is optional and defaults to `True` (descending order, newest first).

Example:

```python
from src.processing import sort_by_date

ops = [
    {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
]

print(sort_by_date(ops))
# -> sorted by date descending (default)

print(sort_by_date(ops, reverse=False))
# -> sorted by date ascending (oldest first)
```

---

## Code Quality Checks

Run formatters/linters/tests (commands may depend on your configuration):

### Run Flake8

```bash
poetry run flake8
```

### Run mypy

```bash
poetry run mypy src
```

### Run pytest

```bash
poetry run pytest
```

---

## GitFlow Workflow (Short Overview)

* `main`: stable branch
* `develop`: integration branch
* `feature/*`: development branches for each task

Work is done in a `feature/...` branch and then merged into `develop` via a Pull Request.

## Testing

Run unit tests:

```bash
poetry run pytest
