from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_operations(path: str | Path) -> list[dict[str, Any]]:
    """
    Load operations from a JSON file.

    Args:
        path: Path to a JSON file.

    Returns:
        A list of dictionaries with operation data. If the file is missing, empty,
        invalid JSON, or JSON root is not a list, returns an empty list.
    """
    file_path = Path(path)

    try:
        text = file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return []

    if not text.strip():
        return []

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []

    if not isinstance(data, list):
        return []

    result: list[dict[str, Any]] = []
    for item in data:
        if isinstance(item, dict):
            result.append(item)

    return result
