from finam_trade_api.account.model import (
    GetAccountResponse,
    GetTradesRequest,
    GetTradesResponse,
    GetTransactionsRequest,
    GetTransactionsResponse,
)
from finam_trade_api.base_client import BaseClient
from finam_trade_api.base_client.token_manager import TokenManager
from finam_trade_api.exceptions import FinamTradeApiError
from finam_trade_api.models import ErrorModel


class AccountClient(BaseClient):
    """
    A client for interacting with account-related endpoints of the Finam Trade API.

    Inherits from:
        BaseClient: Provides base functionality for API requests.

    Attributes:
        _url (str): Base URL for account-related API endpoints.
    """

    def __init__(self, token_manager: TokenManager):
        """
        Initializes the AccountClient.

        Args:
            token_manager (TokenManager): Manages authentication tokens for API requests.
        """
        super().__init__(token_manager)
        self._url = "/accounts"

    async def get_account_info(self, account_id: str) -> GetAccountResponse:
        """
        Retrieves information about a specific account.

        Args:
            account_id (str): The ID of the account to retrieve information for.

        Returns:
            GetAccountResponse: Parsed response containing account information.

        Raises:
            FinamTradeApiError: If the API request fails or returns an error.
        """
        response, ok = await self._exec_request(
            self.RequestMethod.GET,
            f"{self._url}/{account_id}",
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(f"code={err.code} | message={err.message} | details={err.details}")

        return GetAccountResponse(**response)

    async def get_transactions(self, params: GetTransactionsRequest) -> GetTransactionsResponse:
        """
        Retrieves a list of transactions for a specific account.

        Args:
            params (GetTransactionsRequest): Parameters for the request, including account ID, time interval, and limit.

        Returns:
            GetTransactionsResponse: Parsed response containing transaction details.

        Raises:
            FinamTradeApiError: If the API request fails or returns an error.
        """
        response, ok = await self._exec_request(
            self.RequestMethod.GET,
            f"{self._url}/{params.account_id}/transactions",
            params={
                "interval.start_time": params.start_time,
                "interval.end_time": params.end_time,
                "limit": params.limit,
            }
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(f"code={err.code} | message={err.message} | details={err.details}")

        return GetTransactionsResponse(**response)

    async def get_trades(self, params: GetTradesRequest) -> GetTradesResponse:
        """
        Retrieves a list of trades for a specific account.

        Args:
            params (GetTradesRequest): Parameters for the request, including account ID, time interval, and limit.

        Returns:
            GetTradesResponse: Parsed response containing trade details.

        Raises:
            FinamTradeApiError: If the API request fails or returns an error.
        """
        response, ok = await self._exec_request(
            self.RequestMethod.GET,
            f"{self._url}/{params.account_id}/trades",
            params={
                "interval.start_time": params.start_time,
                "interval.end_time": params.end_time,
                "limit": params.limit,
            }
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(f"code={err.code} | message={err.message} | details={err.details}")

        return GetTradesResponse(**response)
