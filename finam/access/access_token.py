from finam.access.model import TokenResponseModel
from finam.base_client.base import BaseClient
from finam.exceptions import FinamTradeApiError
from finam.models import ErrorBodyModel


class TokenClient(BaseClient):
    def __init__(self, token: str):
        super().__init__(token)
        self._url = "/api/v1/access-tokens"

    async def check_token(self):
        response, ok = await self._exec_request(
            self.RequestMethod.GET,
            f"{self._url}/check",
        )
        if not ok:
            err = ErrorBodyModel(**response)
            raise FinamTradeApiError(f"{err.error.code} | {err.error.data} | {err.error.message}")
        return TokenResponseModel(**response)
