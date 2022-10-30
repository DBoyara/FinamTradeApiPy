from finam.base_client.base import BaseClient
from finam.portfolio.model import PortfolioRequestModel, PortfolioResponseModel


class PortfolioClient(BaseClient):
    def __init__(self, token: str):
        super().__init__(token)
        self._portfolio_url = "api/v1/portfolio"

    async def get_portfolio(self, params: PortfolioRequestModel) -> PortfolioResponseModel:
        params = {
            "ClientId": params.client_id,
            "Content.IncludeCurrencies": str(params.include_currencies),
            "Content.IncludeMoney": str(params.include_money),
            "Content.IncludePositions": str(params.include_positions),
            "Content.IncludeMaxBuySell": str(params.include_maxBuySell),
        }
        response = await self._exec_request(self.RequestMethod.GET, self._portfolio_url, params=params)
        return PortfolioResponseModel(**response)
