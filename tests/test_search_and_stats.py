from __future__ import annotations

from typing import Any

import pytest

from src.search_and_stats import process_bank_operations, process_bank_search


@pytest.fixture()
def operations() -> list[dict[str, Any]]:
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Перевод со счета на счет"},
        {"id": 3, "description": "Открытие вклада"},
        {"id": 4, "description": "Перевод с карты на карту"},
        {"id": 5, "description": "перевод организации"},  # absichtlich andere Groß-/Kleinschreibung
        {"id": 6},  # keine description
        {"id": 7, "description": None},  # falscher Typ
    ]


@pytest.mark.parametrize(
    ("search", "expected_ids"),
    [
        ("перевод", [1, 2, 4, 5]),
        ("ОРГАНИЗАЦИИ", [1, 5]),
        ("вклада", [3]),
        ("не найдено", []),
        ("", []),
    ],
)
def test_process_bank_search(operations: list[dict[str, Any]], search: str, expected_ids: list[int]) -> None:
    result = process_bank_search(operations, search)
    assert [item["id"] for item in result] == expected_ids


def test_process_bank_operations_counts(operations: list[dict[str, Any]]) -> None:
    categories = ["перевод", "вклада", "организации"]
    result = process_bank_operations(operations, categories)

    # перевод: IDs 1,2,4,5 -> 4
    assert result["перевод"] == 4
    # вклада: ID 3 -> 1
    assert result["вклада"] == 1
    # организации: IDs 1,5 -> 2
    assert result["организации"] == 2


def test_process_bank_operations_empty_categories(operations: list[dict[str, Any]]) -> None:
    assert process_bank_operations(operations, []) == {}
