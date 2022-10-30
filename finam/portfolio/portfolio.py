from finam.base_client.base import BaseClient
from finam.portfolio.model import PortfolioRequestModel, PortfolioResponseModel


class PortfolioClient(BaseClient):
    def __init__(self, token: str):
        super().__init__(token)
        self._portfolio_url = "api/v1/portfolio"

    async def get_portfolio(self, params: PortfolioRequestModel) -> PortfolioResponseModel:
        r = await self._exec_request(self.RequestMethod.GET, self._portfolio_url, params=params.json(by_alias=True))
        return PortfolioResponseModel(**r)
