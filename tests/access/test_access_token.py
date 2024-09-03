from unittest.mock import AsyncMock, patch

import pytest

from finam_trade_api.access.access_token import TokenClient
from finam_trade_api.access.model import TokenResponseModel
from finam_trade_api.exceptions import FinamTradeApiError
from finam_trade_api.models import ErrorBodyModel


@pytest.fixture
def token_client():
    token = "sample_token"
    return TokenClient(token)


@pytest.mark.asyncio
async def test_token_client_initialization(token_client):
    assert token_client._url == "/api/v1/access-tokens"


@pytest.mark.asyncio
async def test_check_token_success(token_client):
    response_data = {
        "data": {
            "id": 12345,
        }
    }
    token_response = TokenResponseModel(**response_data)

    with patch.object(token_client, '_exec_request', new=AsyncMock(return_value=(response_data, True))):
        response = await token_client.check_token()
        assert response == token_response


@pytest.mark.asyncio
async def test_check_token_error(token_client):
    error_data = {
        "error": {
            "code": "invalid_token",
            "message": "The token is invalid"
        }
    }
    error_response = ErrorBodyModel(**error_data)

    with patch.object(token_client, '_exec_request', new=AsyncMock(return_value=(error_data, False))):
        with pytest.raises(FinamTradeApiError) as excinfo:
            await token_client.check_token()
        assert str(
            excinfo.value) == f"{error_response.error.code} | {error_response.error.data} | {error_response.error.message}"
