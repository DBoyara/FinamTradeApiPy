from finam_trade_api import TokenManager
from finam_trade_api.base_client import BaseClient
from finam_trade_api.exceptions import FinamTradeApiError
from finam_trade_api.models import ErrorModel
from finam_trade_api.order.model import (
    CancelOrderRequest,
    GetOrderRequest,
    Order,
    OrdersRequest,
    OrdersResponse,
    OrderState,
)


class OrderClient(BaseClient):
    def __init__(self, token_manager: TokenManager):
        super().__init__(token_manager)
        self._url = "/accounts"


    async def get_orders(self, params: OrdersRequest) -> OrdersResponse:
        """
        Получение списка заявок для аккаунта.

        Args:
            params (OrdersRequest): Параметры запроса с идентификатором аккаунта.

        Returns:
            OrdersResponse: Список торговых заявок.

        Raises:
            FinamTradeApiError: Если запрос завершился с ошибкой.
        """
        response, ok = await self._exec_request(
            self.RequestMethod.GET,
            f"{self._url}/{params.account_id}/orders",
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(f"code={err.code} | message={err.message} | details={err.details}")

        return OrdersResponse(**response)


    async def get_order(self, params: GetOrderRequest) -> OrderState:
        """
        Получение информации о конкретном ордере.

        Args:
            params (GetOrderRequest): Параметры запроса с идентификатором аккаунта и заявки.

        Returns:
            OrderState: Состояние заявки.

        Raises:
            FinamTradeApiError: Если запрос завершился с ошибкой.
        """
        response, ok = await self._exec_request(
            self.RequestMethod.GET,
            f"{self._url}/{params.account_id}/orders/{params.order_id}",
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(f"code={err.code} | message={err.message} | details={err.details}")

        return OrderState(**response)


    async def place_order(self, order: Order) -> OrderState:
        """
        Выставление биржевой заявки.

        Args:
            order (Order): Информация о заявке для выставления.

        Returns:
            OrderState: Состояние созданной заявки.

        Raises:
            FinamTradeApiError: Если запрос завершился с ошибкой.
        """
        # Используем model_dump с mode='json' для корректной сериализации enum'ов
        payload = order.model_dump(mode="json", exclude_none=True)

        response, ok = await self._exec_request(
            self.RequestMethod.POST,
            f"{self._url}/{order.account_id}/orders",
            payload=payload,
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(f"code={err.code} | message={err.message} | details={err.details}")

        return OrderState(**response)


    async def cancel_order(self, params: CancelOrderRequest) -> OrderState:
        """
        Отмена биржевой заявки.

        Args:
            params (CancelOrderRequest): Параметры запроса с идентификатором аккаунта и заявки.

        Returns:
            OrderState: Состояние отмененной заявки.

        Raises:
            FinamTradeApiError: Если запрос завершился с ошибкой.
        """
        response, ok = await self._exec_request(
            self.RequestMethod.DELETE,
            f"{self._url}/{params.account_id}/orders/{params.order_id}",
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(f"code={err.code} | message={err.message} | details={err.details}")

        return OrderState(**response)
