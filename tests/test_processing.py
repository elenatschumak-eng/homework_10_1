import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture()
def operations():
    # bewusst gemischt: EXECUTED + CANCELED + fehlender state
    return [
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 3, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 4, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 5, "date": "2020-01-01T00:00:00.000000"},  # kein "state"
    ]


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 2]),
        ("CANCELED", [3, 4]),
        ("PENDING", []),
    ],
)
def test_filter_by_state_parametrized(operations, state, expected_ids):
    result = filter_by_state(operations, state=state)
    assert [item["id"] for item in result] == expected_ids


def test_filter_by_state_default_is_executed(operations):
    # Default-Argument soll EXECUTED filtern
    result = filter_by_state(operations)
    assert [item["id"] for item in result] == [1, 2]


def test_filter_by_state_empty_list():
    assert filter_by_state([]) == []


def test_filter_by_state_missing_state_key_is_ignored(operations):
    # Ein Element ohne "state" darf nicht crashen und soll nicht im Ergebnis landen
    result = filter_by_state(operations, state="EXECUTED")
    assert all("state" in item for item in result)


def test_sort_by_date_default_descending(operations):
    # reverse=True ist Default => absteigend (neueste zuerst)
    result = sort_by_date(operations)
    dates = [item.get("date") for item in result]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_ascending_when_reverse_false(operations):
    result = sort_by_date(operations, reverse=False)
    dates = [item.get("date") for item in result]
    assert dates == sorted(dates, reverse=False)


def test_sort_by_date_same_dates_keeps_all_items():
    ops = [
        {"id": 1, "state": "EXECUTED", "date": "2019-01-01T00:00:00.000000"},
        {"id": 2, "state": "EXECUTED", "date": "2019-01-01T00:00:00.000000"},
    ]
    result = sort_by_date(ops)
    assert {item["id"] for item in result} == {1, 2}
