import logging
from datetime import datetime
from pathlib import Path

from src.masks import get_mask_account
from src.masks import get_mask_card_number

LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOGS_DIR / "widget.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

if not logger.handlers:
    logger.addHandler(file_handler)


def mask_account_card(input_number: str) -> str:
    """Mask a card or account number inside a string."""
    logger.debug("mask_account_card called")

    proved_input_number = input_number.strip()
    if not proved_input_number:
        logger.error("Input is empty in mask_account_card")
        raise ValueError("Input is empty.")

    splitted_input_number = proved_input_number.split()
    if len(splitted_input_number) < 2:
        logger.error("Input must contain a name and a number. Input=%r", proved_input_number)
        raise ValueError("Input must contain a name and a number.")

    number_str = splitted_input_number[-1]
    name_str = " ".join(splitted_input_number[:-1])

    if not number_str.isdigit():
        logger.error("Number part contains non-digit characters. number=%r", number_str)
        raise ValueError("Input must contain digits only.")

    name_lower = name_str.lower()
    is_account = name_lower in {"счет", "счёт"}

    if is_account:
        logger.debug("Detected account: name=%r", name_str)
        masked_number = get_mask_account(int(number_str))
    else:
        logger.debug("Detected card: name=%r", name_str)
        masked_number = get_mask_card_number(int(number_str))

    logger.info("mask_account_card success for name=%r", name_str)
    return f"{name_str} {masked_number}"


def get_date(value: str) -> str:
    """Convert 'YYYY-MM-DDTHH:MM:SS.ssssss' to 'DD.MM.YYYY'"""
    logger.debug("get_date called with value=%r", value)

    try:
        dt = datetime.fromisoformat(value)
    except ValueError as exc:
        logger.error("Invalid date format: %r", value)
        raise ValueError("Invalid date format.") from exc

    result = dt.strftime("%d.%m.%Y")
    logger.info("get_date success: %r -> %r", value, result)
    return result
