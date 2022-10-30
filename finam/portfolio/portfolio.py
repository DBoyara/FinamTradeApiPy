from finam.base_client.base import BaseClient
from finam.portfolio.model import PortfolioRequestModel, PortfolioResponseModel


class Portfolio(BaseClient):
    def __init__(self, token: str):
        super().__init__(token)
        self._portfolio_url = "api/v1/portfolio"

    async def get_portfolio(self, params: PortfolioRequestModel) -> PortfolioResponseModel:
        params = {
            "ClientId": params.client_id,
            "Content.IncludeCurrencies": params.includeCurrencies,
            "Content.IncludeMoney": params.includeMoney,
            "Content.IncludePositions": params.includePositions,
            "Content.IncludeMaxBuySell": params.includeMaxBuySell,
        }
        response = await self._exec_request(self.RequestMethod.GET, self._portfolio_url, params=params)
        return PortfolioResponseModel(**response)
