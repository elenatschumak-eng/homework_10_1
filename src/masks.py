def get_mask_card_number(card_number: int) -> str:
    """Return a masked card number in the format 'XXXX XX** **** XXXX'.
    Example: 7000792289606361 -> 7000 79** **** 6361"""

    card_str = str(card_number).strip().replace(" ", "")  # allow input with spaces

    if not card_str.isdigit():
        raise ValueError("Card number must contain digits only.")

    if len(card_str) != 16:
        raise ValueError("Card number must be exactly 16 digits long.")

    masked_card_str = card_str[:6] + ("*" * 6) + card_str[-4:]

    return " ".join(masked_card_str[i: i + 4] for i in range(0, len(masked_card_str), 4))


def get_mask_account(account_number: int | str) -> str:
    """Return a masked account number in the format '**XXXX'.
    Example: 73654108430135874305 -> **4305"""

    account_str = str(account_number).strip().replace(" ", "")  # allow input with spaces

    if not account_str.isdigit():
        raise ValueError("Account number must contain digits only.")

    if len(account_str) < 4:
        raise ValueError("Account number is too short.")
    return "**" + account_str[-4:]
