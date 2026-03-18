from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOGS_DIR / "external_api.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

if not logger.handlers:
    logger.addHandler(file_handler)


def convert_to_rub(transaction: dict[str, Any]) -> float:
    """
    Convert a transaction amount to RUB.

    If currency is RUB, returns the amount as float.
    If currency is USD or EUR, fetches current rate via Exchange Rates Data API (apilayer)
    and converts amount to RUB.

    Args:
        transaction: Transaction dictionary.

    Returns:
        Amount in RUB as float.

    Raises:
        ValueError: If amount/currency is missing or invalid.
        RuntimeError: If API key is missing or API request fails.
    """
    logger.debug("convert_to_rub called")

    operation_amount = transaction.get("operationAmount")
    if not isinstance(operation_amount, dict):
        logger.error("Missing or invalid 'operationAmount'")
        raise ValueError("Missing or invalid 'operationAmount'.")

    amount_str = operation_amount.get("amount")
    currency = operation_amount.get("currency")

    if not isinstance(amount_str, str):
        logger.error("Missing or invalid 'amount'")
        raise ValueError("Missing or invalid 'amount'.")

    if not isinstance(currency, dict):
        logger.error("Missing or invalid 'currency'")
        raise ValueError("Missing or invalid 'currency'.")

    code = currency.get("code")
    if not isinstance(code, str):
        logger.error("Missing or invalid currency code")
        raise ValueError("Missing or invalid currency code.")

    amount = float(amount_str)
    logger.debug("Parsed amount=%s code=%s", amount, code)

    if code == "RUB":
        logger.info("No conversion needed (RUB). amount=%s", amount)
        return amount

    if code not in {"USD", "EUR"}:
        logger.error("Unsupported currency: %s", code)
        raise ValueError(f"Unsupported currency: {code}")

    api_key = os.getenv("APILAYER_API_KEY")
    if not api_key:
        logger.error("Missing APILAYER_API_KEY in environment")
        raise RuntimeError("Missing APILAYER_API_KEY in environment.")

    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers: dict[str, str] = {"apikey": api_key}
    params: dict[str, str | float] = {"from": code, "to": "RUB", "amount": amount, }

    logger.info("Requesting conversion %s -> RUB for amount=%s", code, amount)

    resp = requests.get(url, headers=headers, params=params, timeout=10)
    logger.debug("API response status=%s", resp.status_code)

    if resp.status_code != 200:
        logger.error("API request failed status=%s body=%s", resp.status_code, resp.text)
        raise RuntimeError(f"API request failed with status {resp.status_code}: {resp.text}")

    data = resp.json()
    result = data.get("result")
    if not isinstance(result, (int, float)):
        logger.error("API response missing numeric 'result'")
        raise RuntimeError("API response does not contain numeric 'result'.")

    logger.info("Conversion successful result_rub=%s", float(result))
    return float(result)
