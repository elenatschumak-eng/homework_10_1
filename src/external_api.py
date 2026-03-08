from __future__ import annotations

import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


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
    operation_amount = transaction.get("operationAmount")
    if not isinstance(operation_amount, dict):
        raise ValueError("Missing or invalid 'operationAmount'.")

    amount_str = operation_amount.get("amount")
    currency = operation_amount.get("currency")

    if not isinstance(amount_str, str):
        raise ValueError("Missing or invalid 'amount'.")

    if not isinstance(currency, dict):
        raise ValueError("Missing or invalid 'currency'.")

    code = currency.get("code")
    if not isinstance(code, str):
        raise ValueError("Missing or invalid currency code.")

    amount = float(amount_str)

    if code == "RUB":
        return amount

    if code not in {"USD", "EUR"}:
        raise ValueError(f"Unsupported currency: {code}")

    api_key = os.getenv("APILAYER_API_KEY")
    if not api_key:
        raise RuntimeError("Missing APILAYER_API_KEY in environment.")

    # Exchange Rates Data API (apilayer)
    # We request conversion directly to RUB for the given amount.
    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = {"apikey": api_key}
    params = {"from": code, "to": "RUB", "amount": amount}

    resp = requests.get(url, headers=headers, params=params, timeout=10)
    if resp.status_code != 200:
        raise RuntimeError(f"API request failed with status {resp.status_code}: {resp.text}")

    data = resp.json()
    result = data.get("result")
    if not isinstance(result, (int, float)):
        raise RuntimeError("API response does not contain numeric 'result'.")

    return float(result)
