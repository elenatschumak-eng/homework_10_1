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