from finam_trade_api.access import TokenClient
from finam_trade_api.candles import CandlesClient
from finam_trade_api.order import OrderClient
from finam_trade_api.portfolio import PortfolioClient
from finam_trade_api.securities import SecurityClient


class Client:
    def __init__(self, token: str):
        self.portfolio = PortfolioClient(token)
        self.securities = SecurityClient(token)
        self.orders = OrderClient(token)
        self.access_tokens = TokenClient(token)
        self.candles = CandlesClient(token)
