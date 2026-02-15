from __future__ import annotations

from collections.abc import Iterator
from typing import Any

Transaction = dict[str, Any]


def filter_by_currency(
    transactions: list[dict[str, Any]],
    currency: str,
) -> Iterator[dict[str, Any]]:
    """Yield transactions whose operationAmount currency matches the given currency (by code or name)."""
    currency_upper = currency.upper()

    for tx in transactions:
        if not isinstance(tx, dict):
            continue

        op_amount = tx.get("operationAmount")
        if not isinstance(op_amount, dict):
            # z.B. "wrong_type" -> überspringen, aber NICHT abbrechen
            continue

        cur = op_amount.get("currency")
        if not isinstance(cur, dict):
            continue

        code = cur.get("code")
        name = cur.get("name")

        if isinstance(code, str) and code.upper() == currency_upper:
            yield tx
            continue

        if isinstance(name, str) and name.upper() == currency_upper:
            yield tx


def transaction_descriptions(transactions: list[Transaction]) -> Iterator[str]:
    """Yield the 'description' field from each transaction in order.

    Args:
        transactions: List of transaction dictionaries.

    Yields:
        Descriptions as strings (only if description is a string).
    """
    for tx in transactions:
        desc = tx.get("description")
        if isinstance(desc, str):
            yield desc


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """Generate card numbers in 'XXXX XXXX XXXX XXXX' format (inclusive range).

    Args:
        start: Start number (inclusive).
        stop: Stop number (inclusive).

    Yields:
        Formatted card numbers with leading zeros.

    Raises:
        ValueError: If start/stop are negative or start > stop.
    """
    if start < 0 or stop < 0:
        raise ValueError("start and stop must be non-negative.")
    if start > stop:
        raise ValueError("start must be <= stop.")

    for num in range(start, stop + 1):
        digits = f"{num:016d}"
        yield f"{digits[0:4]} {digits[4:8]} {digits[8:12]} {digits[12:16]}"
