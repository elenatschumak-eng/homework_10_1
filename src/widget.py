from datetime import datetime

from src.masks import get_mask_account
from src.masks import get_mask_card_number


def mask_account_card(input_number: str) -> str:
    """Mask a card or account number inside a string."""
    proved_input_number = input_number.strip()
    if not proved_input_number:
        raise ValueError("Input is empty.")

    splitted_input_number = proved_input_number.split()
    if len(splitted_input_number) < 2:
        raise ValueError("Input must contain a name and a number.")

    number_str = splitted_input_number[-1]
    name_str = " ".join(splitted_input_number[:-1])

    if not number_str.isdigit():
        raise ValueError("Input must contain digits only.")

    name_lower = name_str.lower()
    is_account = name_lower in {"счет", "счёт"}

    if is_account:
        masked_number = get_mask_account(int(number_str))
    else:
        masked_number = get_mask_card_number(int(number_str))

    return f"{name_str} {masked_number}"


def get_date(value: str) -> str:
    """Convert 'YYYY-MM-DDTHH:MM:SS.ssssss' to 'DD.MM.YYYY'"""
    try:
        dt = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("Invalid date format.") from exc

    return dt.strftime("%d.%m.%Y")
