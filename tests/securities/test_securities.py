from unittest.mock import AsyncMock, patch

import pytest

from finam_trade_api.exceptions import FinamTradeApiError
from finam_trade_api.securities.model import SecurityResponseModel
from finam_trade_api.securities.securities import SecurityClient


@pytest.fixture
def security_client():
    return SecurityClient(token="test_token")


@pytest.fixture
def mock_response():
    return {
        "data": {
            "securities": [
                {
                    "code": "TEST_CODE",
                    "board": "TQBR",
                    "market": "Stock",
                    "decimals": 2,
                    "lotSize": 10,
                    "minStep": 1,
                    "properties": 1,
                    "bpCost": 10,
                    "accruedInterest": 10,
                    "priceSign": "priceSign",
                    "ticker": "SBER",
                    "lotDivider": 1
                }
            ],
        }
    }


@pytest.mark.asyncio
async def test_security_client_initialization(security_client):
    assert security_client._url == "/api/v1/securities"
    assert security_client._params == {}


@pytest.mark.asyncio
async def test_get_data_with_code(security_client, mock_response):
    with patch.object(security_client, '_exec_request', new=AsyncMock(return_value=(mock_response, True))):
        response = await security_client.get_data(code="TEST_CODE")
        assert response == SecurityResponseModel(**mock_response)
        assert security_client._params["seccode"] == "TEST_CODE"


@pytest.mark.asyncio
async def test_get_data_with_board(security_client, mock_response):
    with patch.object(security_client, '_exec_request', new=AsyncMock(return_value=(mock_response, True))):
        response = await security_client.get_data(board="TQBR")
        assert response == SecurityResponseModel(**mock_response)
        assert security_client._params["board"] == "TQBR"


@pytest.mark.asyncio
async def test_get_data_with_code_and_board(security_client, mock_response):
    with patch.object(security_client, '_exec_request', new=AsyncMock(return_value=(mock_response, True))):
        response = await security_client.get_data(code="TEST_CODE", board="TQBR")
        assert response == SecurityResponseModel(**mock_response)
        assert security_client._params["seccode"] == "TEST_CODE"
        assert security_client._params["board"] == "TQBR"


@pytest.mark.asyncio
async def test_get_data_error_handling(security_client):
    mock_error_response = {
        "error": {
            "code": "ERROR_CODE",
            "data": None,
            "message": "ERROR_MESSAGE"
        }
    }
    with patch.object(security_client, '_exec_request', new=AsyncMock(return_value=(mock_error_response, False))):
        with pytest.raises(FinamTradeApiError) as exc_info:
            await security_client.get_data(code="TEST_CODE")
        assert str(exc_info.value) == "ERROR_CODE | None | ERROR_MESSAGE"
