from finam_trade_api.base_client import BaseClient
from finam_trade_api.base_client.token_manager import TokenManager
from finam_trade_api.exceptions import FinamTradeApiError
from finam_trade_api.models import ErrorModel
from finam_trade_api.quotas.model import QuotasResponse


class QuotasClient(BaseClient):
    """
    Attributes:
        _url (str): Base URL for the instruments API.
    """

    def __init__(self, token_manager: TokenManager):
        """
        Initializes the QuotasClient.

        Args:
            token_manager (TokenManager): An instance of TokenManager for handling authentication tokens.
        """
        super().__init__(token_manager)
        self._url = "/usage"

    async def get_quotas(self) -> QuotasResponse:
        """
        Retrieves quotas.

        Returns:
            QuotasResponse: The response containing the usage data.

        Raises:
            FinamTradeApiError: If the API request fails.
        """
        response, ok = await self._exec_request(
            self.RequestMethod.GET,
            self._url,
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(f"code={err.code} | message={err.message} | details={err.details}")

        return QuotasResponse(**response)
