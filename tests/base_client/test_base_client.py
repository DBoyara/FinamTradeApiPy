from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, timedelta

import pytest

from finam_trade_api.base_client.base import BaseClient
from finam_trade_api.base_client.token_manager import TokenManager
from finam_trade_api.access.access_token import TokenClient


@pytest.fixture
def base_client():
    token = "test_token"
    return BaseClient(TokenManager(token))


@pytest.mark.asyncio
async def test_base_client_initialization(base_client):
    assert base_client._base_url == "https://api.finam.ru/v1"


@pytest.mark.asyncio
@patch('httpx.AsyncClient')
async def test_exec_request_success(mock_session, base_client):
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.headers = {"content-type": "application/json"}
    mock_response.json = Mock(return_value={"key": "value"})

    mock_session_instance = mock_session.return_value
    mock_session_instance.__aenter__.return_value = mock_session_instance
    mock_session_instance.request = AsyncMock(return_value=mock_response)

    response, success = await base_client._exec_request("get", "/test-url")
    assert success is True
    assert response == {"key": "value"}


@pytest.mark.asyncio
@patch('httpx.AsyncClient')
async def test_exec_request_failure(mock_session, base_client):
    mock_response = AsyncMock()
    mock_response.status_code = 404
    mock_response.headers = {"content-type": "application/json"}
    mock_response.json = Mock(return_value={"error": "not found"})

    mock_session_instance = mock_session.return_value
    mock_session_instance.__aenter__.return_value = mock_session_instance
    mock_session_instance.request = AsyncMock(return_value=mock_response)

    response, success = await base_client._exec_request("get", "/test-url")
    assert success is False
    assert response == {"error": "not found"}


@pytest.mark.asyncio
@patch('httpx.AsyncClient')
async def test_exec_request_auto_refresh_on_401(mock_session, base_client):
    """Тест автоматического обновления токена при получении ошибки 401"""
    # Создаем мок для TokenClient
    token_client = AsyncMock(spec=TokenClient)
    token_client.set_jwt_token = AsyncMock()
    base_client.set_token_client(token_client)

    # Первый ответ - 401 (неавторизован)
    mock_response_401 = AsyncMock()
    mock_response_401.status_code = 401
    mock_response_401.headers = {"content-type": "application/json"}
    mock_response_401.json = Mock(return_value={"error": "unauthorized"})

    # Второй ответ - 200 (успех после обновления токена)
    mock_response_200 = AsyncMock()
    mock_response_200.status_code = 200
    mock_response_200.headers = {"content-type": "application/json"}
    mock_response_200.json = Mock(return_value={"key": "value"})

    mock_session_instance = mock_session.return_value
    mock_session_instance.__aenter__.return_value = mock_session_instance
    # Первый запрос возвращает 401, второй - 200
    mock_session_instance.request = AsyncMock(side_effect=[mock_response_401, mock_response_200])

    response, success = await base_client._exec_request("get", "/test-url")

    # Проверяем, что токен был обновлен
    token_client.set_jwt_token.assert_called_once()
    # Проверяем, что получили успешный ответ
    assert success is True
    assert response == {"key": "value"}
    # Проверяем, что было сделано 2 запроса (первый с ошибкой, второй успешный)
    assert mock_session_instance.request.call_count == 2


@pytest.mark.asyncio
@patch('httpx.AsyncClient')
async def test_exec_request_preventive_refresh(mock_session, base_client):
    """Тест превентивного обновления токена каждые 10 минут"""
    # Создаем мок для TokenClient
    token_client = AsyncMock(spec=TokenClient)
    token_client.set_jwt_token = AsyncMock()
    base_client.set_token_client(token_client)

    # Устанавливаем время последнего обновления в прошлом (более 10 минут назад)
    base_client._last_token_refresh = datetime.now() - timedelta(minutes=11)

    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.headers = {"content-type": "application/json"}
    mock_response.json = Mock(return_value={"key": "value"})

    mock_session_instance = mock_session.return_value
    mock_session_instance.__aenter__.return_value = mock_session_instance
    mock_session_instance.request = AsyncMock(return_value=mock_response)

    response, success = await base_client._exec_request("get", "/test-url")

    # Проверяем, что токен был обновлен превентивно
    token_client.set_jwt_token.assert_called_once()
    assert success is True
    assert response == {"key": "value"}


@pytest.mark.asyncio
@patch('httpx.AsyncClient')
async def test_exec_request_no_refresh_when_recent(mock_session, base_client):
    """Тест что токен не обновляется, если недавно был обновлен"""
    # Создаем мок для TokenClient
    token_client = AsyncMock(spec=TokenClient)
    token_client.set_jwt_token = AsyncMock()
    base_client.set_token_client(token_client)

    # Устанавливаем время последнего обновления недавно (менее 10 минут назад)
    base_client._last_token_refresh = datetime.now() - timedelta(minutes=5)

    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.headers = {"content-type": "application/json"}
    mock_response.json = Mock(return_value={"key": "value"})

    mock_session_instance = mock_session.return_value
    mock_session_instance.__aenter__.return_value = mock_session_instance
    mock_session_instance.request = AsyncMock(return_value=mock_response)

    response, success = await base_client._exec_request("get", "/test-url")

    # Проверяем, что токен НЕ был обновлен
    token_client.set_jwt_token.assert_not_called()
    assert success is True
    assert response == {"key": "value"}


@pytest.mark.asyncio
async def test_should_refresh_token_when_never_refreshed(base_client):
    """Тест что токен должен быть обновлен, если никогда не обновлялся"""
    assert base_client._should_refresh_token() is True


@pytest.mark.asyncio
async def test_should_refresh_token_when_expired(base_client):
    """Тест что токен должен быть обновлен, если прошло более 10 минут"""
    base_client._last_token_refresh = datetime.now() - timedelta(minutes=11)
    assert base_client._should_refresh_token() is True


@pytest.mark.asyncio
async def test_should_not_refresh_token_when_recent(base_client):
    """Тест что токен не должен быть обновлен, если обновлялся недавно"""
    base_client._last_token_refresh = datetime.now() - timedelta(minutes=5)
    assert base_client._should_refresh_token() is False
