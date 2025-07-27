import pytest
from unittest.mock import AsyncMock, patch

from finam_trade_api.instruments.instruments import InstrumentClient
from finam_trade_api.instruments.model import (
    BarsRequest,
    BarsResponse,
    QuoteResponse,
    TradesResponse,
    OrderBookResponse,
    TimeFrame,
)
from finam_trade_api.exceptions import FinamTradeApiError


@pytest.fixture
def token_manager():
    tm = AsyncMock()
    tm.token = "valid_token"
    return tm


@pytest.fixture
def instrument_client(token_manager):
    return InstrumentClient(token_manager)


@pytest.mark.asyncio
async def test_get_bars_success(instrument_client):
    params = BarsRequest(
        symbol="SBER",
        start_time="2025-01-01T00:00:00Z",
        end_time="2025-01-02T00:00:00Z",
        timeframe=TimeFrame.TIME_FRAME_D,
    )
    response_data = {"symbol": "SBER", "bars": []}
    with patch.object(instrument_client, "_exec_request", return_value=(response_data, True)) as mock_exec:
        result = await instrument_client.get_bars(params)
        mock_exec.assert_called_once_with(
            instrument_client.RequestMethod.GET,
            f"/instruments/{params.symbol}/bars",
            params={
                "timeframe": params.timeframe.value,
                "interval.start_time": params.start_time,
                "interval.end_time": params.end_time,
            },
        )
        assert isinstance(result, BarsResponse)
        assert result.symbol == "SBER"


@pytest.mark.asyncio
async def test_get_bars_failure(instrument_client):
    params = BarsRequest(
        symbol="SBER",
        start_time="2025-01-01T00:00:00Z",
        end_time="2025-01-02T00:00:00Z",
        timeframe=TimeFrame.TIME_FRAME_D,
    )
    error_response = {"code": 400, "message": "Bad Request", "details": []}
    with patch.object(instrument_client, "_exec_request", return_value=(error_response, False)) as mock_exec:
        with pytest.raises(FinamTradeApiError, match="code=400 | message=Bad Request"):
            await instrument_client.get_bars(params)
        mock_exec.assert_called_once()


@pytest.mark.asyncio
async def test_get_last_quote_success(instrument_client):
    symbol = "SBER"
    response_data = {"symbol": symbol, "quote": {
        "symbol": "YDEX@MISX",
        "timestamp": "2025-05-16T12:07:21.464413Z",
        "ask": {
            "value": "4030.5"
        },
        "ask_size": {
            "value": "90"
        },
        "bid": {
            "value": "4030.0"
        },
        "bid_size": {
            "value": "25"
        },
        "last": {
            "value": "4030.5"
        },
        "last_size": {
            "value": "39"
        },
        "volume": {
            "value": "169596"
        },
        "turnover": {
            "value": "6.8042089E8"
        },
        "open": {
            "value": "3998.0"
        },
        "high": {
            "value": "4034.5"
        },
        "low": {
            "value": "3984.5"
        },
        "close": {
            "value": "3989.5"
        },
        "change": {
            "value": "41.0"
        }
    }}
    with patch.object(instrument_client, "_exec_request", return_value=(response_data, True)) as mock_exec:
        result = await instrument_client.get_last_quote(symbol)
        mock_exec.assert_called_once_with(
            instrument_client.RequestMethod.GET,
            f"/instruments/{symbol}/quotes/latest",
        )
        assert isinstance(result, QuoteResponse)
        assert result.symbol == symbol


@pytest.mark.asyncio
async def test_get_last_quote_failure(instrument_client):
    symbol = "SBER"
    error_response = {"code": 404, "message": "Not Found", "details": []}
    with patch.object(instrument_client, "_exec_request", return_value=(error_response, False)) as mock_exec:
        with pytest.raises(FinamTradeApiError, match="code=404 | message=Not Found"):
            await instrument_client.get_last_quote(symbol)
        mock_exec.assert_called_once()


@pytest.mark.asyncio
async def test_get_last_trades_success(instrument_client):
    symbol = "SBER"
    response_data = {"symbol": symbol, "trades": []}
    with patch.object(instrument_client, "_exec_request", return_value=(response_data, True)) as mock_exec:
        result = await instrument_client.get_last_trades(symbol)
        mock_exec.assert_called_once_with(
            instrument_client.RequestMethod.GET,
            f"/instruments/{symbol}/trades/latest",
        )
        assert isinstance(result, TradesResponse)
        assert result.symbol == symbol


@pytest.mark.asyncio
async def test_get_last_trades_failure(instrument_client):
    symbol = "SBER"
    error_response = {"code": 500, "message": "Internal Server Error", "details": []}
    with patch.object(instrument_client, "_exec_request", return_value=(error_response, False)) as mock_exec:
        with pytest.raises(FinamTradeApiError, match="code=500 | message=Internal Server Error"):
            await instrument_client.get_last_trades(symbol)
        mock_exec.assert_called_once()


@pytest.mark.asyncio
async def test_get_order_book_success(instrument_client):
    symbol = "SBER"
    response_data = {"symbol": symbol, "orderbook": {"rows": []}}
    with patch.object(instrument_client, "_exec_request", return_value=(response_data, True)) as mock_exec:
        result = await instrument_client.get_order_book(symbol)
        mock_exec.assert_called_once_with(
            instrument_client.RequestMethod.GET,
            f"/instruments/{symbol}/orderbook",
        )
        assert isinstance(result, OrderBookResponse)
        assert result.symbol == symbol


@pytest.mark.asyncio
async def test_get_order_book_failure(instrument_client):
    symbol = "SBER"
    error_response = {"code": 403, "message": "Forbidden", "details": []}
    with patch.object(instrument_client, "_exec_request", return_value=(error_response, False)) as mock_exec:
        with pytest.raises(FinamTradeApiError, match="code=403 | message=Forbidden"):
            await instrument_client.get_order_book(symbol)
        mock_exec.assert_called_once()
