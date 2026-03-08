import logging
from pathlib import Path

LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOGS_DIR / "masks.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

if not logger.handlers:
    logger.addHandler(file_handler)


def get_mask_card_number(card_number: int) -> str:
    """Return a masked card number in the format 'XXXX XX** **** XXXX'.
    Example: 7000792289606361 -> 7000 79** **** 6361"""

    logger.debug("Masking card number")

    card_str = str(card_number).strip().replace(" ", "")  # allow input with spaces

    if not card_str.isdigit():
        logger.error("Invalid card number: contains non-digit characters")
        raise ValueError("Card number must contain digits only.")

    if len(card_str) != 16:
        logger.error("Invalid card number length: %d", len(card_str))
        raise ValueError("Card number must be exactly 16 digits long.")

    masked_card_str = card_str[:6] + ("*" * 6) + card_str[-4:]

    logger.info("Card number masked successfully")

    return " ".join(masked_card_str[i: i + 4] for i in range(0, len(masked_card_str), 4))


def get_mask_account(account_number: int | str) -> str:
    """Return a masked account number in the format '**XXXX'.
    Example: 73654108430135874305 -> **4305"""

    logger.debug("Masking account number")

    account_str = str(account_number).strip().replace(" ", "")  # allow input with spaces

    if not account_str.isdigit():
        logger.error("Invalid account number: contains non-digit characters")
        raise ValueError("Account number must contain digits only.")

    if len(account_str) < 4:
        logger.error("Invalid account number length: %d", len(account_str))
        raise ValueError("Account number is too short.")
    logger.info("Account number masked successfully")
    return "**" + account_str[-4:]
