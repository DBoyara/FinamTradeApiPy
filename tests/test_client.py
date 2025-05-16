import pytest

from finam_trade_api.access.access_token import TokenClient
from finam_trade_api.instruments.instruments import InstrumentClient
from finam_trade_api.client import Client
from finam_trade_api.account.account import AccountClient
from finam_trade_api.assets.assets import AssetsClient
from finam_trade_api.base_client.token_manager import TokenManager


@pytest.fixture
def client():
    token = "your_token_here"
    return Client(TokenManager(token))


def test_client_initialization(client):
    assert isinstance(client.account, AccountClient)
    assert isinstance(client.assets, AssetsClient)
    # assert isinstance(client.orders, OrderClient)
    assert isinstance(client.access_tokens, TokenClient)
    assert isinstance(client.instruments, InstrumentClient)
