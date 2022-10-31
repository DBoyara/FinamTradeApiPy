from typing import Union

from finam.base_client.base import BaseClient
from finam.models import ErrorBodyModel
from finam.order.model import (
    OrdersRequestModel,
    OrdersResponseModel,
    DelOrderModel,
    CreateOrderRequestModel,
    CreateOrderResponseModel,
    DelOrderResponseModel
)


class OrderClient(BaseClient):
    def __init__(self, token: str):
        super().__init__(token)
        self._order_url = "/api/v1/orders"
        self._stop_order_url = "/api/v1/stop-orders"

    async def get_orders(self, params: OrdersRequestModel) -> Union[OrdersResponseModel, ErrorBodyModel]:
        response, ok = await self._exec_request(
            self.RequestMethod.GET,
            self._order_url,
            params=params.dict(exclude_none=True)
        )
        if not ok:
            return ErrorBodyModel(**response)
        return OrdersResponseModel(**response)

    async def create_order(self, payload: CreateOrderRequestModel) -> Union[CreateOrderResponseModel, ErrorBodyModel]:
        response, ok = await self._exec_request(
            self.RequestMethod.POST,
            self._order_url,
            payload.dict(exclude_none=True)
        )
        if not ok:
            return ErrorBodyModel(**response)
        return CreateOrderResponseModel(**response)

    async def del_order(self, params: DelOrderModel) -> Union[DelOrderResponseModel, ErrorBodyModel]:
        response, ok = await self._exec_request(
            self.RequestMethod.DELETE,
            self._order_url,
            params=params.dict()
        )
        if not ok:
            return ErrorBodyModel(**response)
        return DelOrderResponseModel(**response)
