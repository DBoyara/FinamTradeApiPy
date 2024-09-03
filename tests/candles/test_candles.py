from unittest.mock import AsyncMock, patch

import pytest

from finam_trade_api.candles.candles import CandlesClient
from finam_trade_api.candles.model import (
    DayCandle,
    DayCandlesRequestModel,
    DayCandlesResponse,
    IntraDayCandle,
    IntraDayCandlesRequestModel,
    IntraDayCandlesResponse,
)
from finam_trade_api.exceptions import FinamTradeApiError
from finam_trade_api.models import ErrorBodyModel


@pytest.fixture
def candles_client():
    token = "sample_token"
    return CandlesClient(token)


@pytest.mark.asyncio
async def test_candles_client_initialization(candles_client):
    assert candles_client._day_url == "/api/v1/day-candles"
    assert candles_client._in_day_url == "/api/v1/intraday-candles"


@pytest.mark.asyncio
async def test_get_day_candles_success(candles_client):
    params = DayCandlesRequestModel(
        securityBoard="board",
        securityCode="code",
        timeFrame="D1",
        intervalFrom="2023-01-01",
        intervalTo="2023-01-02",
        count=10
    )
    response_data = {
        "data": {
            "candles": [
                {
                    "date": "2020-02-02",
                    "open": {"num": 100, "scale": 0},
                    "close": {"num": 110, "scale": 0},
                    "high": {"num": 115, "scale": 0},
                    "low": {"num": 95, "scale": 0},
                    "volume": 1000
                }
            ]
        }
    }
    day_candles_response = DayCandlesResponse(**response_data)

    with patch.object(candles_client, '_exec_request', new=AsyncMock(return_value=(response_data, True))):
        response = await candles_client.get_day_candles(params)
        assert response == day_candles_response.data.candles


@pytest.mark.asyncio
async def test_get_day_candles_error(candles_client):
    params = DayCandlesRequestModel(
        securityBoard="board",
        securityCode="code",
        timeFrame="D1",
        intervalFrom="2023-01-01",
        intervalTo="2023-01-02",
        count=10
    )
    error_data = {
        "error": {
            "code": "invalid_request",
            "message": "Invalid request parameters"
        }
    }
    error_response = ErrorBodyModel(**error_data)

    with patch.object(candles_client, '_exec_request', new=AsyncMock(return_value=(error_data, False))):
        with pytest.raises(FinamTradeApiError) as excinfo:
            await candles_client.get_day_candles(params)
        assert str(
            excinfo.value) == f"{error_response.error.code} | {error_response.error.data} | {error_response.error.message}"


@pytest.mark.asyncio
async def test_get_in_day_candles_success(candles_client):
    params = IntraDayCandlesRequestModel(
        securityBoard="board",
        securityCode="code",
        timeFrame="M5",
        intervalFrom="2023-01-01",
        intervalTo="2023-01-02",
        count=10
    )
    response_data = {
        "data": {
            "candles": [
                {
                    "timestamp": "2020-02-02 00:00:00",
                    "open": {"num": 100, "scale": 0},
                    "close": {"num": 110, "scale": 0},
                    "high": {"num": 115, "scale": 0},
                    "low": {"num": 95, "scale": 0},
                    "volume": 1000
                }
            ]
        }
    }
    in_day_candles_response = IntraDayCandlesResponse(**response_data)

    with patch.object(candles_client, '_exec_request', new=AsyncMock(return_value=(response_data, True))):
        response = await candles_client.get_in_day_candles(params)
        assert response == in_day_candles_response.data.candles


@pytest.mark.asyncio
async def test_get_in_day_candles_error(candles_client):
    params = IntraDayCandlesRequestModel(
        securityBoard="board",
        securityCode="code",
        timeFrame="M1",
        intervalFrom="2023-01-01",
        intervalTo="2023-01-02",
        count=10
    )
    error_data = {
        "error": {
            "code": "invalid_request",
            "message": "Invalid request parameters"
        }
    }
    error_response = ErrorBodyModel(**error_data)

    with patch.object(candles_client, '_exec_request', new=AsyncMock(return_value=(error_data, False))):
        with pytest.raises(FinamTradeApiError) as excinfo:
            await candles_client.get_in_day_candles(params)
        assert str(
            excinfo.value) == f"{error_response.error.code} | {error_response.error.data} | {error_response.error.message}"