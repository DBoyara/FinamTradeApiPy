from typing import Optional, Union

from finam_trade_api.base_client import BaseClient
from finam_trade_api.exceptions import FinamTradeApiError
from finam_trade_api.models import ErrorBodyModel
from finam_trade_api.securities.model import Security, SecurityResponseModel


class SecurityClient(BaseClient):
    def __init__(self, token: str):
        super().__init__(token)
        self._url = "/api/v1/securities"

    async def get_data(self, code: Optional[str] = None) -> Union[SecurityResponseModel, Security, ErrorBodyModel]:
        response, ok = await self._exec_request(self.RequestMethod.GET, self._url)
        if not ok:
            err = ErrorBodyModel(**response)
            raise FinamTradeApiError(f"{err.error.code} | {err.error.data} | {err.error.message}")
        s = SecurityResponseModel(**response)
        if code:
            for security in s.data.securities:
                if security.code.lower() != code.lower():
                    continue
                return security
        return s
