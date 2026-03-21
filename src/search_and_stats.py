from __future__ import annotations

import re
from collections import Counter
from typing import Any


def process_bank_search(data: list[dict[str, Any]], search: str) -> list[dict[str, Any]]:
    """
    Search operations by a substring in the 'description' field using regular expressions.

    Args:
        data: List of operations (dictionaries).
        search: Search string.

    Returns:
        List of operations where 'description' contains the search string.
    """
    if not search:
        return []

    pattern = re.compile(re.escape(search), re.IGNORECASE)

    result: list[dict[str, Any]] = []
    for op in data:
        desc = op.get("description")
        if isinstance(desc, str) and pattern.search(desc):
            result.append(op)

    return result


def process_bank_operations(data: list[dict[str, Any]], categories: list[str]) -> dict[str, int]:
    """
    Count how many operations match each category (by substring match in 'description').

    Uses collections.Counter.

    Args:
        data: List of operations (dictionaries).
        categories: List of category strings to search for in descriptions.

    Returns:
        Dict: {category: count}
    """
    if not categories:
        return {}

    patterns = {cat: re.compile(re.escape(cat), re.IGNORECASE) for cat in categories if cat}
    counter: Counter[str] = Counter({cat: 0 for cat in categories if cat})

    for op in data:
        desc = op.get("description")
        if not isinstance(desc, str):
            continue

        for cat, pat in patterns.items():
            if pat.search(desc):
                counter[cat] += 1

    return dict(counter)
