from __future__ import annotations

from functools import wraps

from collections.abc import Callable
from typing import Any


def log(filename: str | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator that logs function execution.

    If `filename` is provided, logs are appended to that file.
    If `filename` is None, logs are printed to the console.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def write(message: str) -> None:
            if filename:
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(message + "\n")
            else:
                print(message)

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                write(f"{func.__name__} ok")
                return result
            except Exception as exc:
                write(f"{func.__name__} error: {type(exc).__name__}. Inputs: {args}, {kwargs}")
                raise

        return wrapper

    return decorator
