from finam_trade_api.assets.model import ExchangesResponse, OptionsChainResponse, ScheduleResponse
from finam_trade_api.base_client import BaseClient
from finam_trade_api.base_client.token_manager import TokenManager
from finam_trade_api.exceptions import FinamTradeApiError
from finam_trade_api.models import ErrorModel


class AssetsClient(BaseClient):
    """
    Клиент для работы с счетами через API Finam Trade.

    Args:
        token_manager (TokenManager): Менеджер токенов для авторизации запросов.
    """
    def __init__(self, token_manager: TokenManager):
        """
        Инициализация клиента счетов.

        Args:
            token_manager (TokenManager): Менеджер токенов для авторизации запросов.
        """
        super().__init__(token_manager)
        self._url = "/assets"
        self._exchanges_url = "/exchanges"

    async def get_exchanges(self) -> ExchangesResponse:
        """
        Получение списка доступных бирж, включая их названия и MIC-коды.

        Returns:
            ExchangesResponse: Ответ API с информацией о биржах.

        Raises:
            FinamTradeApiError: Если запрос завершился с ошибкой.
        """
        response, ok = await self._exec_request(
            self.RequestMethod.GET,
            self._exchanges_url,
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(f"code={err.code} | message={err.message} | details={err.details}")

        return ExchangesResponse(**response)

    async def get_assets(self):
        """
        Получение списка доступных инструментов, их описание

        Returns:
            NotImplementedError: Метод не реализован.
        """
        raise NotImplementedError

    async def get_asset_params(self, symbol: str, account_id: str):
        """
        Получение торговых параметров по инструменту

        Args:
            symbol (str): Символ инструмента.
            account_id (str): Идентификатор аккаунта.

        Returns:
            NotImplementedError: Метод не реализован.
        """
        raise NotImplementedError

    async def get_options_chain(self, underlying_symbol: str) -> OptionsChainResponse:
        """
        Получение цепочки опционов для базового актива.

        Args:
            underlying_symbol (str): Символ базового актива.

        Returns:
            OptionsChainResponse: Ответ API с информацией о цепочке опционов.

        Raises:
            FinamTradeApiError: Если запрос завершился с ошибкой.
        """
        response, ok = await self._exec_request(
            self.RequestMethod.GET,
            f"{self._url}/{underlying_symbol}/options",
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(f"code={err.code} | message={err.message} | details={err.details}")

        return OptionsChainResponse(**response)

    async def get_schedule(self, symbol: str) -> ScheduleResponse:
        """
        Получение расписания торгов для указанного инструмента.

        Args:
            symbol (str): Символ инструмента.

        Returns:
            ScheduleResponse: Ответ API с информацией о расписании торгов.

        Raises:
            FinamTradeApiError: Если запрос завершился с ошибкой.
        """
        response, ok = await self._exec_request(
            self.RequestMethod.GET,
            f"{self._url}/{symbol}/schedule",
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(f"code={err.code} | message={err.message} | details={err.details}")

        return ScheduleResponse(**response)
