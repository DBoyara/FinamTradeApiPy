from typing import Union

from finam_trade_api.base_client import BaseClient
from finam_trade_api.exceptions import FinamTradeApiError
from finam_trade_api.models import ErrorBodyModel
from finam_trade_api.portfolio.model import (
    PortfolioRequestModel,
    PortfolioResponseModel
)


class PortfolioClient(BaseClient):
    def __init__(self, token: str):
        super().__init__(token)
        self._url = "/api/v1/portfolio"

    async def get_portfolio(self, params: PortfolioRequestModel) -> Union[PortfolioResponseModel, ErrorBodyModel]:
        p = {
            "clientId": params.clientId,
            "content.IncludeCurrencies": params.includeCurrencies,
            "content.IncludeMoney": params.includeMoney,
            "content.IncludePositions": params.includePositions,
            "content.IncludeMaxBuySell": params.includeMaxBuySell,
        }
        response, ok = await self._exec_request(self.RequestMethod.GET, self._url, params=p)
        if not ok:
            err = ErrorBodyModel(**response)
            raise FinamTradeApiError(f"{err.error.code} | {err.error.data} | {err.error.message}")
        return PortfolioResponseModel(**response)
