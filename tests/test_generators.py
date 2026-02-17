import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


@pytest.fixture()
def transactions():
    # bewusst gemischt: USD/RUB, fehlende Felder, falsche Typen
    return [
        {
            "id": 1,
            "operationAmount": {"amount": "10.00", "currency": {"name": "USD", "code": "USD"}},
            "description": "Payment USD 1",
        },
        {
            "id": 2,
            "operationAmount": {"amount": "20.00", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Payment RUB",
        },
        {
            "id": 3,
            "operationAmount": {"amount": "30.00", "currency": {"name": "USD", "code": "USD"}},
            "description": "Payment USD 2",
        },
        {"id": 4, "description": "No operationAmount"},
        {"id": 5, "operationAmount": "wrong_type", "description": "Bad operationAmount type"},
        {"id": 6, "operationAmount": {"currency": "wrong_type"}, "description": "Bad currency type"},
        {"id": 7, "operationAmount": {"currency": {"code": "USD"}}, "description": None},
    ]


@pytest.mark.parametrize(
    ("currency", "expected_ids"),
    [
        ("USD", [1, 3, 7]),
        ("RUB", [2]),
        ("EUR", []),
    ],
)
def test_filter_by_currency(transactions, currency, expected_ids):
    gen = filter_by_currency(transactions, currency)
    result = list(gen)
    assert [item["id"] for item in result] == expected_ids


def test_filter_by_currency_empty_list():
    assert list(filter_by_currency([], "USD")) == []


def test_transaction_descriptions(transactions):
    gen = transaction_descriptions(transactions)
    result = list(gen)
    # nur str-Descriptions werden yielded; None wird übersprungen
    assert result == [
        "Payment USD 1",
        "Payment RUB",
        "Payment USD 2",
        "No operationAmount",
        "Bad operationAmount type",
        "Bad currency type",
    ]


def test_transaction_descriptions_empty_list():
    assert list(transaction_descriptions([])) == []


@pytest.mark.parametrize(
    ("start", "stop", "expected"),
    [
        (1, 1, ["0000 0000 0000 0001"]),
        (1, 5, [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005",
        ]),
        (9999, 10000, ["0000 0000 0000 9999", "0000 0000 0001 0000"]),
    ],
)
def test_card_number_generator_range(start, stop, expected):
    assert list(card_number_generator(start, stop)) == expected


def test_card_number_generator_includes_stop():
    assert list(card_number_generator(5, 5)) == ["0000 0000 0000 0005"]
