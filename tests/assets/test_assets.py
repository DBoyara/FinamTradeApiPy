import pytest
from unittest.mock import AsyncMock, patch

from finam_trade_api.assets.assets import AssetsClient
from finam_trade_api.exceptions import FinamTradeApiError
from finam_trade_api.assets.model import ExchangesResponse, OptionsChainResponse, ScheduleResponse


@pytest.fixture
def token_manager():
    tm = AsyncMock()
    tm.token = "valid_token"
    return tm


@pytest.fixture
def assets_client(token_manager):
    return AssetsClient(token_manager)


@pytest.mark.asyncio
async def test_get_exchanges_success(assets_client):
    response_data = {"exchanges": [{"mic": "MIC123", "name": "Test Exchange"}]}
    with patch.object(assets_client, "_exec_request", return_value=(response_data, True)) as mock_exec:
        result = await assets_client.get_exchanges()
        mock_exec.assert_called_once_with(assets_client.RequestMethod.GET, "/exchanges")
        assert isinstance(result, ExchangesResponse)
        assert result.exchanges[0].mic == "MIC123"


@pytest.mark.asyncio
async def test_get_exchanges_failure(assets_client):
    error_response = {"code": 404, "message": "Not Found", "details": []}
    with patch.object(assets_client, "_exec_request", return_value=(error_response, False)) as mock_exec:
        with pytest.raises(FinamTradeApiError, match="code=404 | message=Not Found"):
            await assets_client.get_exchanges()
        mock_exec.assert_called_once()


@pytest.mark.asyncio
async def test_get_options_chain_success(assets_client):
    underlying_symbol = "AAPL"
    response_data = {
        "symbol": underlying_symbol,
        "options": [{
            "symbol": "AAPL2022-12-31C150",
            "type": "call",
            "contractSize": {"value": "1.0"},
            "tradeLastDay": {"year":2022, "month": 12, "day": 31},
            "strike": {"value": "150.0"},
        }]
    }
    with patch.object(assets_client, "_exec_request", return_value=(response_data, True)) as mock_exec:
        result = await assets_client.get_options_chain(underlying_symbol)
        mock_exec.assert_called_once_with(assets_client.RequestMethod.GET, f"/assets/{underlying_symbol}/options")
        assert isinstance(result, OptionsChainResponse)
        assert result.symbol == underlying_symbol
        assert len(result.options) == 1


@pytest.mark.asyncio
async def test_get_options_chain_failure(assets_client):
    underlying_symbol = "AAPL"
    error_response = {"code": 500, "message": "Internal Error", "details": []}
    with patch.object(assets_client, "_exec_request", return_value=(error_response, False)) as mock_exec:
        with pytest.raises(FinamTradeApiError, match="code=500 | message=Internal Error"):
            await assets_client.get_options_chain(underlying_symbol)
        mock_exec.assert_called_once()


@pytest.mark.asyncio
async def test_get_schedule_success(assets_client):
    symbol = "AAPL"
    response_data = {
        "symbol": symbol,
        "sessions": [{
            "type": "regular",
            "interval": {"startTime": "2023-01-01T09:30:00", "endTime": "2023-01-01T16:00:00"}
        }]
    }
    with patch.object(assets_client, "_exec_request", return_value=(response_data, True)) as mock_exec:
        result = await assets_client.get_schedule(symbol)
        mock_exec.assert_called_once_with(assets_client.RequestMethod.GET, f"/assets/{symbol}/schedule")
        assert isinstance(result, ScheduleResponse)
        assert result.symbol == symbol


@pytest.mark.asyncio
async def test_get_schedule_failure(assets_client):
    symbol = "AAPL"
    error_response = {"code": 400, "message": "Bad Request", "details": []}
    with patch.object(assets_client, "_exec_request", return_value=(error_response, False)) as mock_exec:
        with pytest.raises(FinamTradeApiError, match="code=400 | message=Bad Request"):
            await assets_client.get_schedule(symbol)
        mock_exec.assert_called_once()


@pytest.mark.asyncio
async def test_get_assets_not_implemented(assets_client):
    with pytest.raises(NotImplementedError):
        await assets_client.get_assets()


@pytest.mark.asyncio
async def test_get_asset_params_not_implemented(assets_client):
    with pytest.raises(NotImplementedError):
        await assets_client.get_asset_params("AAPL", "account123")
