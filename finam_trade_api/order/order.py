from finam_trade_api import TokenManager
from finam_trade_api.base_client import BaseClient


class OrderClient(BaseClient):
    def __init__(self, token_manager: TokenManager):
        super().__init__(token_manager)
        self._url = "/accounts"

    async def get_orders(self):
        raise NotImplementedError

    async def get_order(self):
        raise NotImplementedError

    async def place_order(self):
        raise NotImplementedError

    async def cancel_order(self):
        raise NotImplementedError
