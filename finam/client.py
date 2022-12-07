from finam.access.access_token import TokenClient
from finam.events.event import EventClient
from finam.order.order import OrderClient
from finam.portfolio.portfolio import PortfolioClient
from finam.securities.securities import SecurityClient


class Client:
    def __init__(self, token: str):
        self.portfolio = PortfolioClient(token)
        self.securities = SecurityClient(token)
        self.orders = OrderClient(token)
        self.event = EventClient(token)
        self.access_tokens = TokenClient(token)
