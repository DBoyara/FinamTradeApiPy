from finam_trade_api.base_client import BaseClient
from finam_trade_api.base_client.token_manager import TokenManager
from finam_trade_api.exceptions import FinamTradeApiError
from finam_trade_api.instruments.model import (
    BarsRequest,
    BarsResponse,
    OrderBookResponse,
    QuoteResponse,
    TradesResponse,
)
from finam_trade_api.models import ErrorModel


class InstrumentClient(BaseClient):
    """
    A client for interacting with the instruments API of the Finam Trade service.
    Provides methods to retrieve market data such as bars, quotes, trades, and order books.

    Attributes:
        _url (str): Base URL for the instruments API.
    """

    def __init__(self, token_manager: TokenManager):
        """
        Initializes the InstrumentClient.

        Args:
            token_manager (TokenManager): An instance of TokenManager for handling authentication tokens.
        """
        super().__init__(token_manager)
        self._url = "/instruments"

    async def get_bars(self, params: BarsRequest) -> BarsResponse:
        """
        Retrieves historical bar data for a given symbol.

        Args:
            params (BarsRequest): Parameters for the bars request, including symbol, timeframe, and interval.

        Returns:
            BarsResponse: The response containing the bar data.

        Raises:
            FinamTradeApiError: If the API request fails.
        """
        response, ok = await self._exec_request(
            self.RequestMethod.GET,
            f"{self._url}/{params.symbol}/bars",
            params={
                "timeframe": params.timeframe.value,
                "interval.start_time": params.start_time,
                "interval.end_time": params.end_time,
            },
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(f"code={err.code} | message={err.message} | details={err.details}")

        return BarsResponse(**response)

    async def get_last_quote(self, symbol: str) -> QuoteResponse:
        """
        Retrieves the latest quote for a given symbol.

        Args:
            symbol (str): The symbol for which to retrieve the latest quote.

        Returns:
            QuoteResponse: The response containing the latest quote.

        Raises:
            FinamTradeApiError: If the API request fails.
        """
        response, ok = await self._exec_request(
            self.RequestMethod.GET,
            f"{self._url}/{symbol}/quotes/latest",
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(f"code={err.code} | message={err.message} | details={err.details}")

        return QuoteResponse(**response)

    async def get_last_trades(self, symbol: str) -> TradesResponse:
        """
        Retrieves the latest trades for a given symbol.

        Args:
            symbol (str): The symbol for which to retrieve the latest trades.

        Returns:
            TradesResponse: The response containing the latest trades.

        Raises:
            FinamTradeApiError: If the API request fails.
        """
        response, ok = await self._exec_request(
            self.RequestMethod.GET,
            f"{self._url}/{symbol}/trades/latest",
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(f"code={err.code} | message={err.message} | details={err.details}")

        return TradesResponse(**response)

    async def get_order_book(self, symbol: str) -> OrderBookResponse:
        """
        Retrieves the order book for a given symbol.

        Args:
            symbol (str): The symbol for which to retrieve the order book.

        Returns:
            OrderBookResponse: The response containing the order book.

        Raises:
            FinamTradeApiError: If the API request fails.
        """
        response, ok = await self._exec_request(
            self.RequestMethod.GET,
            f"{self._url}/{symbol}/orderbook",
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(f"code={err.code} | message={err.message} | details={err.details}")

        return OrderBookResponse(**response)
