from finam_trade_api.access import TokenClient
from finam_trade_api.account import AccountClient
from finam_trade_api.base_client.token_manager import TokenManager
from finam_trade_api.candles import CandlesClient
from finam_trade_api.order import OrderClient
from finam_trade_api.securities import SecurityClient


class Client:
    def __init__(self, token_manger: TokenManager):
        self.account = AccountClient(token_manger)
        self.securities = SecurityClient(token_manger)
        self.orders = OrderClient(token_manger)
        self.access_tokens = TokenClient(token_manger)
        self.candles = CandlesClient(token_manger)
