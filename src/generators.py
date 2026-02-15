from __future__ import annotations

from collections.abc import Iterator
from typing import Any


def filter_by_currency(
    transactions: list[dict[str, Any]],
    currency: str,
) -> Iterator[dict[str, Any]]:
    """
    Yield transactions whose operation currency code matches `currency`.

    Args:
        transactions: List of transaction dictionaries.
        currency: Currency code to filter by (e.g. "USD").

    Yields:
        Transaction dictionaries that match the given currency.
    """
    for tx in transactions:
        operation_amount = tx.get("operationAmount")
        if not isinstance(operation_amount, dict):
            continue

        currency_info = operation_amount.get("currency")
        if not isinstance(currency_info, dict):
            continue

        code = currency_info.get("code")
        if code == currency:
            yield tx


def transaction_descriptions(transactions: list[dict[str, Any]]) -> Iterator[str]:
    """
    Yield the `description` field of each transaction in order.

    Args:
        transactions: List of transaction dictionaries.

    Yields:
        Description strings.
    """
    for tx in transactions:
        description = tx.get("description")
        if isinstance(description, str):
            yield description


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Generate card numbers in the format 'XXXX XXXX XXXX XXXX' for the given range.

    Args:
        start: Start number (inclusive).
        stop: Stop number (inclusive).

    Yields:
        Card numbers formatted with leading zeros and groups of 4 digits.
    """
    for n in range(start, stop + 1):
        digits = f"{n:016d}"
        yield " ".join(digits[i : i + 4] for i in range(0, 16, 4))
