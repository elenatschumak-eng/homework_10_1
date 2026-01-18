from typing import Any


def filter_by_state(operations: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    """    Filter a list of operations by the value of the 'state' key.

    Args:
        operations: List of dictionaries with operation data.
        state: State to filter by. Defaults to 'EXECUTED'.

    Returns:
        A new list containing only operations whose 'state' equals `state`.
    """
    result: list[dict[str, Any]] = []
    for operation in operations:
        if operation.get("state") == state:
            result.append(operation)
    return result


def sort_by_date(operations: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    """Sort a list of operations by the value of the 'date' key.

    Args:
        operations: List of dictionaries with operation data.
        reverse: Whether to sort in descending order. Defaults to True.

    Returns:
        A new list sorted by the 'date' key.
    """
    return sorted(operations, key=lambda op: op.get("date", ""), reverse=reverse)

