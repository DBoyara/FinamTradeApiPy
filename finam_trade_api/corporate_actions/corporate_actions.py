from finam_trade_api.base_client import BaseClient
from finam_trade_api.base_client.models import FinamDate
from finam_trade_api.base_client.token_manager import TokenManager
from finam_trade_api.corporate_actions.model import BondsEventsResponse, SortDirection
from finam_trade_api.exceptions import FinamTradeApiError
from finam_trade_api.models import ErrorModel


class CorporateActionsClient(BaseClient):
    """
    Клиент для работы с корпоративными действиями через API Finam Trade.

    Поддерживает получение календаря событий по облигациям
    (будущих и исторических).

    Args:
        token_manager (TokenManager): Менеджер токенов для авторизации запросов.
    """

    def __init__(self, token_manager: TokenManager):
        """
        Инициализация клиента корпоративных действий.

        Args:
            token_manager (TokenManager): Менеджер токенов для авторизации запросов.
        """
        super().__init__(token_manager)
        self._future_url = "/bonds/future"
        self._past_url = "/bonds/past"

    async def get_future_bonds_events(
        self,
        symbol: str | None = None,
        date_from: FinamDate | None = None,
        date_to: FinamDate | None = None,
        sort_direction: SortDirection | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> BondsEventsResponse:
        """
        Получение календаря будущих событий по облигациям.

        Args:
            symbol (str | None): Символ инструмента.
            date_from (FinamDate | None): Дата начала периода.
            date_to (FinamDate | None): Дата окончания периода.
            sort_direction (SortDirection | None): Направление сортировки.
            limit (int | None): Лимит количества событий.
            offset (int | None): Смещение для пагинации.

        Returns:
            BondsEventsResponse: Ответ API с календарём будущих событий.

        Raises:
            FinamTradeApiError: Если запрос завершился с ошибкой.
        """
        params = self._build_params(symbol, date_from, date_to, sort_direction, limit, offset)
        response, ok = await self._exec_request(
            self.RequestMethod.GET,
            self._future_url,
            params=params,
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(f"code={err.code} | message={err.message} | details={err.details}")

        return BondsEventsResponse(**response)

    async def get_past_bonds_events(
        self,
        symbol: str | None = None,
        date_from: FinamDate | None = None,
        date_to: FinamDate | None = None,
        sort_direction: SortDirection | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> BondsEventsResponse:
        """
        Получение календаря исторических событий по облигациям.

        Args:
            symbol (str | None): Символ инструмента.
            date_from (FinamDate | None): Дата начала периода.
            date_to (FinamDate | None): Дата окончания периода.
            sort_direction (SortDirection | None): Направление сортировки.
            limit (int | None): Лимит количества событий.
            offset (int | None): Смещение для пагинации.

        Returns:
            BondsEventsResponse: Ответ API с календарём исторических событий.

        Raises:
            FinamTradeApiError: Если запрос завершился с ошибкой.
        """
        params = self._build_params(symbol, date_from, date_to, sort_direction, limit, offset)
        response, ok = await self._exec_request(
            self.RequestMethod.GET,
            self._past_url,
            params=params,
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(f"code={err.code} | message={err.message} | details={err.details}")

        return BondsEventsResponse(**response)

    @staticmethod
    def _build_params(
        symbol: str | None,
        date_from: FinamDate | None,
        date_to: FinamDate | None,
        sort_direction: SortDirection | None,
        limit: int | None,
        offset: int | None,
    ) -> dict[str, str | int]:
        """
        Собирает словарь query-параметров, исключая None-значения.

        Композитные даты (date_from, date_to) разворачиваются
        в формат API: date_from.year, date_from.month, date_from.day.

        Returns:
            dict: Словарь параметров запроса.
        """
        params: dict[str, str | int] = {}

        if symbol:
            params["symbol"] = symbol

        if date_from:
            params["date_from.year"] = date_from.year
            params["date_from.month"] = date_from.month
            params["date_from.day"] = date_from.day

        if date_to:
            params["date_to.year"] = date_to.year
            params["date_to.month"] = date_to.month
            params["date_to.day"] = date_to.day

        if sort_direction:
            params["sort_direction"] = sort_direction.value

        if limit:
            params["limit"] = limit

        if offset:
            params["offset"] = offset

        return params
