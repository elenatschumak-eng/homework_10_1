from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOGS_DIR / "utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

if not logger.handlers:
    logger.addHandler(file_handler)


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

    logger.debug("Attempting to load operations from file: %s", file_path)

    try:
        text = file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        logger.error("File not found: %s", file_path)
        return []

    if not text.strip():
        logger.warning("File is empty: %s", file_path)
        return []

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        logger.error("Invalid JSON in file %s: %s", file_path, exc)
        return []

    if not isinstance(data, list):
        logger.error("JSON root is not a list in file: %s", file_path)
        return []

    result: list[dict[str, Any]] = []
    skipped_items = 0

    for item in data:
        if isinstance(item, dict):
            result.append(item)
        else:
            skipped_items += 1

    if skipped_items > 0:
        logger.warning("Skipped %d non-dict items while reading %s", skipped_items, file_path)

    logger.info("Loaded %d operations from %s", len(result), file_path)
    return result
