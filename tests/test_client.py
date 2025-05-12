import pytest

from finam_trade_api.access.access_token import TokenClient
from finam_trade_api.candles.candles import CandlesClient
from finam_trade_api.client import Client
from finam_trade_api.order.order import OrderClient
from finam_trade_api.portfolio.portfolio import PortfolioClient
from finam_trade_api.securities.securities import SecurityClient
from finam_trade_api.base_client.token_manager import TokenManager


@pytest.fixture
def client():
    token = "your_token_here"
    return Client(TokenManager(token))


def test_client_initialization(client):
    assert isinstance(client.portfolio, PortfolioClient)
    assert isinstance(client.securities, SecurityClient)
    assert isinstance(client.orders, OrderClient)
    assert isinstance(client.access_tokens, TokenClient)
    assert isinstance(client.candles, CandlesClient)
