from typing import Optional

from finam_trade_api.base_client import BaseClient
from finam_trade_api.exceptions import FinamTradeApiError
from finam_trade_api.models import ErrorBodyModel
from finam_trade_api.securities.model import SecurityResponseModel


class SecurityClient(BaseClient):
    def __init__(self, token: str):
        super().__init__(token)
        self._url = "/api/v1/securities"
        self._params: dict = {}

    async def get_data(
            self,
            code: Optional[str] = None,
            board: Optional[str] = None,
    ) -> SecurityResponseModel:
        if board:
            self._params["board"] = board
        if code:
            self._params["seccode"] = code

        response, ok = await self._exec_request(self.RequestMethod.GET, self._url, params=self._params)
        if not ok:
            err = ErrorBodyModel(**response)
            raise FinamTradeApiError(f"{err.error.code} | {err.error.data} | {err.error.message}")
        return SecurityResponseModel(**response)
