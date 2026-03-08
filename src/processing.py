import logging
from typing import Any
from pathlib import Path

LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOGS_DIR / "processing.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

if not logger.handlers:
    logger.addHandler(file_handler)


def filter_by_state(operations: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    """Filter a list of operations by the value of the 'state' key.

    Args:
        operations: List of dictionaries with operation data.
        state: State to filter by. Defaults to 'EXECUTED'.

    Returns:
        A new list containing only operations whose 'state' equals `state`.
    """
    logger.debug("filter_by_state called with state=%r", state)
    result: list[dict[str, Any]] = []
    for operation in operations:
        if operation.get("state") == state:
            result.append(operation)
    logger.info("filter_by_state result length=%d", len(result))
    return result


def sort_by_date(operations: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    """Sort a list of operations by the value of the 'date' key.

    Args:
        operations: List of dictionaries with operation data.
        reverse: Whether to sort in descending order. Defaults to True.

    Returns:
        A new list sorted by the 'date' key.
    """
    logger.debug("sort_by_date called reverse=%r", reverse)
    result = sorted(operations, key=lambda op: op.get("date", ""), reverse=reverse)
    logger.info("sort_by_date sorted %d items", len(result))
    return result
