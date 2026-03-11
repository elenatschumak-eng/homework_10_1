from __future__ import annotations

import logging
from collections.abc import Iterator
from pathlib import Path
from typing import Any

Transaction = dict[str, Any]

LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOGS_DIR / "generators.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

if not logger.handlers:
    logger.addHandler(file_handler)


def filter_by_currency(
    transactions: list[dict[str, Any]],
    currency: str,
) -> Iterator[dict[str, Any]]:
    """Yield transactions whose operationAmount currency matches the given currency (by code or name)."""
    currency_upper = currency.upper()
    logger.debug("filter_by_currency called currency=%r, items=%d", currency, len(transactions))

    skipped = 0
    matched = 0

    for tx in transactions:
        if not isinstance(tx, dict):
            skipped += 1
            continue

        op_amount = tx.get("operationAmount")
        if not isinstance(op_amount, dict):
            skipped += 1
            continue

        cur = op_amount.get("currency")
        if not isinstance(cur, dict):
            skipped += 1
            continue

        code = cur.get("code")
        name = cur.get("name")

        if isinstance(code, str) and code.upper() == currency_upper:
            matched += 1
            yield tx
            continue

        if isinstance(name, str) and name.upper() == currency_upper:
            matched += 1
            yield tx

    logger.info("filter_by_currency finished currency=%r matched=%d skipped=%d", currency, matched, skipped)


def transaction_descriptions(transactions: list[Transaction]) -> Iterator[str]:
    """Yield the 'description' field from each transaction in order.

    Args:
        transactions: List of transaction dictionaries.

    Yields:
        Descriptions as strings (only if description is a string).
    """
    logger.debug("transaction_descriptions called items=%d", len(transactions))

    yielded = 0
    skipped = 0

    for tx in transactions:
        desc = tx.get("description")
        if isinstance(desc, str):
            yielded += 1
            yield desc
        else:
            skipped += 1

    logger.info("transaction_descriptions finished yielded=%d skipped=%d", yielded, skipped)


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
    logger.debug("card_number_generator called start=%d stop=%d", start, stop)

    if start < 0 or stop < 0:
        logger.error("Invalid range: negative start/stop (start=%d stop=%d)", start, stop)
        raise ValueError("start and stop must be non-negative.")

    if start > stop:
        logger.error("Invalid range: start > stop (start=%d stop=%d)", start, stop)
        raise ValueError("start must be <= stop.")

    total = stop - start + 1
    logger.info("card_number_generator generating %d numbers", total)

    for num in range(start, stop + 1):
        digits = f"{num:016d}"
        yield f"{digits[0:4]} {digits[4:8]} {digits[8:12]} {digits[12:16]}"
