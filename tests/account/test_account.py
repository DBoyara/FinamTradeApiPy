import pytest
from unittest.mock import AsyncMock, patch

from finam_trade_api.account.account import AccountClient
from finam_trade_api.exceptions import FinamTradeApiError
from finam_trade_api.account.model import (
    GetAccountResponse,
    GetTransactionsResponse,
    GetTradesResponse,
    GetTransactionsRequest,
    GetTradesRequest,
)

@pytest.fixture
def token_manager():
    tm = AsyncMock()
    tm.token = "valid_token"
    return tm

@pytest.fixture
def account_client(token_manager):
    return AccountClient(token_manager)

@pytest.mark.asyncio
async def test_get_account_info_success(account_client):
    account_id = "account123"
    # Создаем данные-заглушку на основе модели GetAccountResponse
    response_data = {
        "account_id": account_id,
        "type": "broker",
        "status": "active",
        "equity": {"value": "1000.0"},
        "unrealized_profit": {"value": "50.0"},
        "positions": [],
        "cash": []
    }
    with patch.object(account_client, "_exec_request", return_value=(response_data, True)) as mock_exec:
        result = await account_client.get_account_info(account_id)
        mock_exec.assert_called_once_with(
            account_client.RequestMethod.GET,
            f"/accounts/{account_id}",
        )
        assert isinstance(result, GetAccountResponse)
        assert result.account_id == account_id

@pytest.mark.asyncio
async def test_get_account_info_failure(account_client):
    account_id = "account123"
    error_response = {"code": 404, "message": "Not Found", "details": []}
    with patch.object(account_client, "_exec_request", return_value=(error_response, False)) as mock_exec:
        with pytest.raises(FinamTradeApiError, match="code=404 | message=Not Found"):
            await account_client.get_account_info(account_id)
        mock_exec.assert_called_once()

@pytest.mark.asyncio
async def test_get_transactions_success(account_client):
    params = GetTransactionsRequest(
        account_id="account123",
        start_time="2024-01-01T00:00:00Z",
        end_time="2025-01-01T00:00:00Z",
        limit=10,
    )
    # Данные-заглушка формируются по модели GetTransactionsResponse
    response_data = {
        "transactions": [
            {
                "id": "tx1",
                "category": "deposit",
                "timestamp": "2023-01-01T00:00:00Z",
                "symbol": "AAPL",
                "change": {"currencyCode": "USD", "units": "100", "nanos": 0},
                "trade": None
            }
        ]
    }
    with patch.object(account_client, "_exec_request", return_value=(response_data, True)) as mock_exec:
        result = await account_client.get_transactions(params)
        mock_exec.assert_called_once_with(
            account_client.RequestMethod.GET,
            f"/accounts/{params.account_id}/transactions",
            params={
                "interval.start_time": params.start_time,
                "interval.end_time": params.end_time,
                "limit": params.limit,
            },
        )
        assert isinstance(result, GetTransactionsResponse)
        assert len(result.transactions) == 1
        assert result.transactions[0].id == "tx1"

@pytest.mark.asyncio
async def test_get_transactions_failure(account_client):
    params = GetTransactionsRequest(
        account_id="account123",
        start_time="2024-01-01T00:00:00Z",
        end_time="2025-01-01T00:00:00Z",
        limit=10,
    )
    error_response = {"code": 400, "message": "Bad Request", "details": []}
    with patch.object(account_client, "_exec_request", return_value=(error_response, False)) as mock_exec:
        with pytest.raises(FinamTradeApiError, match="code=400 | message=Bad Request"):
            await account_client.get_transactions(params)
        mock_exec.assert_called_once()

@pytest.mark.asyncio
async def test_get_trades_success(account_client):
    params = GetTradesRequest(
        account_id="account123",
        start_time="2024-01-01T00:00:00Z",
        end_time="2025-01-01T00:00:00Z",
        limit=10,
    )
    # Данные-заглушка формируются по модели GetTradesResponse
    response_data = {
        "trades": [
            {
                "trade_id": "t1",
                "symbol": "AAPL",
                "price": {"value": "150.0"},
                "size": {"value": "10.0"},
                "side": "buy",
                "timestamp": "2023-01-01T00:00:00Z"
            }
        ]
    }
    with patch.object(account_client, "_exec_request", return_value=(response_data, True)) as mock_exec:
        result = await account_client.get_trades(params)
        mock_exec.assert_called_once_with(
            account_client.RequestMethod.GET,
            f"/accounts/{params.account_id}/trades",
            params={
                "interval.start_time": params.start_time,
                "interval.end_time": params.end_time,
                "limit": params.limit,
            },
        )
        assert isinstance(result, GetTradesResponse)
        assert len(result.trades) == 1
        assert result.trades[0].trade_id == "t1"

@pytest.mark.asyncio
async def test_get_trades_failure(account_client):
    params = GetTradesRequest(
        account_id="account123",
        start_time="2024-01-01T00:00:00Z",
        end_time="2025-01-01T00:00:00Z",
        limit=10,
    )
    error_response = {"code": 500, "message": "Internal Server Error", "details": []}
    with patch.object(account_client, "_exec_request", return_value=(error_response, False)) as mock_exec:
        with pytest.raises(FinamTradeApiError, match="code=500 | message=Internal Server Error"):
            await account_client.get_trades(params)
        mock_exec.assert_called_once()
