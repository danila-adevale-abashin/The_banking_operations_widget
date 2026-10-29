from unittest.mock import Mock, patch

import pytest

from src.external_api import get_transaction_amount


@pytest.fixture
def usd_transaction():
    return {"operationAmount": {"amount": "100.0", "currency": {"code": "USD"}}}


@pytest.fixture
def eur_transaction():
    return {"operationAmount": {"amount": "100.0", "currency": {"code": "EUR"}}}


@pytest.fixture
def rub_transaction():
    return {"operationAmount": {"amount": "1000.0", "currency": {"code": "RUB"}}}


# 1. ТЕСТ ДЛЯ USD (успешный)
@patch("src.external_api.requests.request")
def test_usd_success(mock_request, usd_transaction):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 9500.0}
    mock_request.return_value = mock_response

    result = get_transaction_amount(usd_transaction)

    assert result == 9500.0
    mock_request.assert_called_once()

    # Проверяем, что URL собран правильно
    args, kwargs = mock_request.call_args
    assert "from=USD" in args[1]
    assert "amount=100.0" in args[1]


# 2. ТЕСТ ДЛЯ USD (ошибка 401)
@patch("src.external_api.requests.request")
def test_usd_api_error(mock_request, usd_transaction):
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"
    mock_request.return_value = mock_response

    with pytest.raises(RuntimeError, match="API вернул 401"):
        get_transaction_amount(usd_transaction)


# 3. ТЕСТ ДЛЯ EUR (успешный)
@patch("src.external_api.requests.request")
def test_eur_success(mock_request, eur_transaction):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 10500.0}
    mock_request.return_value = mock_response

    result = get_transaction_amount(eur_transaction)

    assert result == 10500.0
    mock_request.assert_called_once()

    args, kwargs = mock_request.call_args
    assert "from=EUR" in args[1]


# 4. ТЕСТ ДЛЯ RUB (без запроса к API)
@patch("src.external_api.requests.request")
def test_rub_no_api_call(mock_request, rub_transaction):
    result = get_transaction_amount(rub_transaction)

    assert result == "1000.0"
    mock_request.assert_not_called()
