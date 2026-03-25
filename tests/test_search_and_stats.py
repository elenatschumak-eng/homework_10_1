import pytest

from src.search_and_stats import process_bank_operations, process_bank_search


@pytest.fixture()
def operations() -> list[dict]:
    # Kleine, kontrollierte Beispieldaten für stabile Tests
    return [
        {"id": 1, "description": "Открытие вклада"},
        {"id": 2, "description": "Перевод со счета на счет"},
        {"id": 3, "description": "Перевод с карты на карту"},
        {"id": 4, "description": None},   # kein String -> muss ignoriert werden
        {"id": 5},                        # kein description -> muss ignoriert werden
    ]


@pytest.mark.parametrize(
    ("query", "expected_ids"),
    [
        ("перевод", [2, 3]),   # case-insensitive Suche
        ("ВКЛАД", [1]),
        ("", []),              # leere Suche -> leere Liste
    ],
)
def test_process_bank_search(operations: list[dict], query: str, expected_ids: list[int]) -> None:
    result = process_bank_search(operations, query)
    assert [item["id"] for item in result] == expected_ids


def test_process_bank_operations_counts(operations: list[dict]) -> None:
    categories = ["Перевод", "вклад", "Кредит"]
    result = process_bank_operations(operations, categories)

    # Keys müssen genau die Kategorien sein, die du übergibst
    assert result["Перевод"] == 2
    assert result["вклад"] == 1
    assert result["Кредит"] == 0


def test_process_bank_operations_empty_categories(operations: list[dict]) -> None:
    assert process_bank_operations(operations, []) == {}
