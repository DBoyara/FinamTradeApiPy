import pytest
from unittest.mock import AsyncMock, patch

from finam_trade_api.assets.assets import AssetsClient
from finam_trade_api.exceptions import FinamTradeApiError
from finam_trade_api.assets.model import ExchangesResponse, OptionsChainResponse, ScheduleResponse, ClockResponse, \
    AssetParamsResponse, AssetResponse, AssetsResponse


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
            "contract_size": {"value": "1.0"},
            "trade_last_day": {"year":2022, "month": 12, "day": 31},
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
            "interval": {"start_time": "2023-01-01T09:30:00", "end_time": "2023-01-01T16:00:00"}
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
async def test_get_asset_success(assets_client):
    symbol = "AAPL"
    account_id = "account123"
    response_data = {"id": "1", "ticker": "AAPL", "mic": "MIC123", "isin": "US0378331005", "type": "stock", "name": "Apple Inc.", "board": "TQBR", "decimals": 2, "min_step": "0.01", "lot_size": {"value": "10"}}
    with patch.object(assets_client, "_exec_request", return_value=(response_data, True)) as mock_exec:
        result = await assets_client.get_asset(symbol, account_id)
        mock_exec.assert_called_once_with(assets_client.RequestMethod.GET, f"/assets/{symbol}", params={"account_id": account_id})
        assert isinstance(result, AssetResponse)
        assert result.ticker == "AAPL"


@pytest.mark.asyncio
async def test_get_asset_failure(assets_client):
    symbol = "AAPL"
    account_id = "account123"
    error_response = {"code": 404, "message": "Not Found", "details": []}
    with patch.object(assets_client, "_exec_request", return_value=(error_response, False)) as mock_exec:
        with pytest.raises(FinamTradeApiError, match="code=404 | message=Not Found"):
            await assets_client.get_asset(symbol, account_id)
        mock_exec.assert_called_once()


@pytest.mark.asyncio
async def test_get_asset_params_success(assets_client):
    symbol = "AAPL"
    account_id = "account123"
    response_data = {"id": "1", "ticker": "AAPL", "mic": "MIC123", "isin": "US0378331005", "type": "stock", "name": "Apple Inc.", "symbol": "AAPL", "account_id": account_id, "tradeable": True, "longable": {"value": "yes", "halted_days": 0}, "shortable": {"value": "no", "halted_days": 0}}
    with patch.object(assets_client, "_exec_request", return_value=(response_data, True)) as mock_exec:
        result = await assets_client.get_asset_params(symbol, account_id)
        mock_exec.assert_called_once_with(assets_client.RequestMethod.GET, f"/assets/{symbol}/params", params={"account_id": account_id})
        assert isinstance(result, AssetParamsResponse)
        assert result.symbol == "AAPL"


@pytest.mark.asyncio
async def test_get_asset_params_failure(assets_client):
    symbol = "AAPL"
    account_id = "account123"
    error_response = {"code": 403, "message": "Forbidden", "details": []}
    with patch.object(assets_client, "_exec_request", return_value=(error_response, False)) as mock_exec:
        with pytest.raises(FinamTradeApiError, match="code=403 | message=Forbidden"):
            await assets_client.get_asset_params(symbol, account_id)
        mock_exec.assert_called_once()


@pytest.mark.asyncio
async def test_get_clock_success(assets_client):
    response_data = {"timestamp": "2023-01-01T12:00:00"}
    with patch.object(assets_client, "_exec_request", return_value=(response_data, True)) as mock_exec:
        result = await assets_client.get_clock()
        mock_exec.assert_called_once_with(assets_client.RequestMethod.GET, "/assets/clock")
        assert isinstance(result, ClockResponse)
        assert result.timestamp.isoformat() == "2023-01-01T12:00:00"


@pytest.mark.asyncio
async def test_get_clock_failure(assets_client):
    error_response = {"code": 400, "message": "Bad Request", "details": []}
    with patch.object(assets_client, "_exec_request", return_value=(error_response, False)) as mock_exec:
        with pytest.raises(FinamTradeApiError, match="code=400 | message=Bad Request"):
            await assets_client.get_clock()
        mock_exec.assert_called_once()
