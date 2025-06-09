from unittest.mock import AsyncMock, patch

import pytest

from finam_trade_api.base_client.base import BaseClient
from finam_trade_api.base_client.token_manager import TokenManager


@pytest.fixture
def base_client():
    token = "test_token"
    return BaseClient(TokenManager(token))


@pytest.mark.asyncio
async def test_base_client_initialization(base_client):
    assert base_client._base_url == "https://api.finam.ru/v1"


@pytest.mark.asyncio
@patch('aiohttp.ClientSession')
async def test_exec_request_success(mock_session, base_client):
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={"key": "value"})

    mock_session_instance = mock_session.return_value
    mock_session_instance.__aenter__.return_value = mock_session_instance
    mock_session_instance.request.return_value.__aenter__.return_value = mock_response

    response, success = await base_client._exec_request("get", "/test-url")
    assert success is True
    assert response == {"key": "value"}


@pytest.mark.asyncio
@patch('aiohttp.ClientSession')
async def test_exec_request_failure(mock_session, base_client):
    mock_response = AsyncMock()
    mock_response.status = 404
    mock_response.json = AsyncMock(return_value={"error": "not found"})

    mock_session_instance = mock_session.return_value
    mock_session_instance.__aenter__.return_value = mock_session_instance
    mock_session_instance.request.return_value.__aenter__.return_value = mock_response

    response, success = await base_client._exec_request("get", "/test-url")
    assert success is False
    assert response == {"error": "not found"}
