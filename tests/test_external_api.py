from typing import Any
from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_to_rub


def test_convert_to_rub_rub_no_api_call() -> None:
    tx = {"operationAmount": {"amount": "10.00", "currency": {"code": "RUB"}}}
    assert convert_to_rub(tx) == 10.0


@patch("src.external_api.os.getenv", return_value="TEST_KEY")
@patch("src.external_api.requests.get")
def test_convert_to_rub_usd_mocked(get_mock: Mock, getenv_mock: Mock) -> None:
    # fake API response
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"result": 1234.5}
    get_mock.return_value = response

    tx = {"operationAmount": {"amount": "10.00", "currency": {"code": "USD"}}}
    result = convert_to_rub(tx)

    assert result == 1234.5
    get_mock.assert_called_once()
    args, kwargs = get_mock.call_args
    assert "convert" in args[0]  # URL
    assert kwargs["headers"]["apikey"] == "TEST_KEY"
    assert kwargs["params"]["from"] == "USD"
    assert kwargs["params"]["to"] == "RUB"
    assert kwargs["params"]["amount"] == 10.0


@patch("src.external_api.os.getenv", return_value=None)
def test_convert_to_rub_missing_api_key(getenv_mock: Mock) -> None:
    tx = {"operationAmount": {"amount": "10.00", "currency": {"code": "USD"}}}
    with pytest.raises(RuntimeError):
        convert_to_rub(tx)


def test_convert_to_rub_invalid_structure() -> None:
    with pytest.raises(ValueError):
        convert_to_rub({})
