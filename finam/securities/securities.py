from typing import Union, Optional

from finam.base_client.base import BaseClient
from finam.models import ErrorBodyModel
from finam.securities.model import SecurityResponseModel, Security


class SecurityClient(BaseClient):
    def __init__(self, token: str):
        super().__init__(token)
        self._securities_url = "/api/v1/securities"

    async def get_data(self, code: Optional[str] = None) -> Union[SecurityResponseModel, Security, ErrorBodyModel]:
        response, ok = await self._exec_request(self.RequestMethod.GET, self._securities_url)
        if not ok:
            return ErrorBodyModel(**response)
        s = SecurityResponseModel(**response)
        if code:
            for security in s.data.securities:
                if security.code != code:
                    continue
                return security
        return s