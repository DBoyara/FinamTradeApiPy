from finam_trade_api.access import TokenClient
from finam_trade_api.account import AccountClient
from finam_trade_api.assets import AssetsClient
from finam_trade_api.base_client.token_manager import TokenManager
from finam_trade_api.instruments import InstrumentClient


class Client:
    def __init__(self, token_manger: TokenManager):
        self.account = AccountClient(token_manger)
        self.assets = AssetsClient(token_manger)
        # self.orders = OrderClient(token_manger)
        self.access_tokens = TokenClient(token_manger)
        self.instruments = InstrumentClient(token_manger)
