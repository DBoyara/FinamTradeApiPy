import pytest

from finam_trade_api.access.access_token import TokenClient
from finam_trade_api.instruments.instruments import InstrumentClient
from finam_trade_api.client import Client
from finam_trade_api.account.account import AccountClient
from finam_trade_api.assets.assets import AssetsClient
from finam_trade_api.base_client.token_manager import TokenManager
from finam_trade_api.order import OrderClient


@pytest.fixture
def client():
    token = "your_token_here"
    return Client(TokenManager(token))


def test_client_initialization(client):
    assert isinstance(client.account, AccountClient)
    assert isinstance(client.assets, AssetsClient)
    assert isinstance(client.orders, OrderClient)
    assert isinstance(client.access_tokens, TokenClient)
    assert isinstance(client.instruments, InstrumentClient)


def test_client_auto_refresh_enabled_by_default():
    """Тест что auto_refresh_tokens=True по умолчанию"""
    token = "your_token_here"
    client = Client(TokenManager(token))
    
    # Проверяем что token_client установлен для всех подклиентов
    assert client.account._token_client is not None
    assert client.assets._token_client is not None
    assert client.orders._token_client is not None
    assert client.instruments._token_client is not None


def test_client_auto_refresh_disabled():
    """Тест что при auto_refresh_tokens=False token_client не устанавливается"""
    token = "your_token_here"
    client = Client(TokenManager(token), auto_refresh_tokens=False)
    
    # Проверяем что token_client НЕ установлен
    assert client.account._token_client is None
    assert client.assets._token_client is None
    assert client.orders._token_client is None
    assert client.instruments._token_client is None
    assert client.quotas._token_client is None
