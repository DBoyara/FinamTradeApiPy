from unittest.mock import AsyncMock, patch

import pytest

from finam_trade_api.order.model import (
    CreateOrderRequestModel,
    CreateOrderResponseModel,
    DelOrderModel,
    DelOrderResponseModel,
    OrdersRequestModel,
    OrdersResponseModel,
)
from finam_trade_api.order.order import OrderClient


class TestOrderClient:

    @pytest.fixture
    def client(self):
        return OrderClient(token="mock_token")

    @pytest.fixture
    def mock_exec_request(self):
        with patch.object(OrderClient, '_exec_request', new_callable=AsyncMock) as mock:
            yield mock

    @pytest.mark.asyncio
    async def test_get_orders(self, client, mock_exec_request):
        mock_response = {"data": {"clientId": "clientId", "orders": []}}
        mock_exec_request.return_value = (mock_response, True)
        params = OrdersRequestModel(clientId="clientId")
        response = await client.get_orders(params)
        assert response == OrdersResponseModel(**mock_response)
        mock_exec_request.assert_called_once_with(
            client.RequestMethod.GET,
            client._order_url,
            params=params.model_dump(exclude_none=True)
        )
        assert response.data.clientId == "clientId"

    @pytest.mark.asyncio
    async def test_create_order(self, client, mock_exec_request):
        mock_response = {"data": {"clientId": "123", "transactionId": 1, "securityCode": "code"}}
        mock_exec_request.return_value = (mock_response, True)
        payload = CreateOrderRequestModel(
            **{
                "clientId": "clientId",
                "securityBoard": "TQBR",
                "securityCode": "code",
                "buySell": "Sell",
                "quantity": 1,
                "property": "PutInQueue"
            }
        )
        response = await client.create_order(payload)
        assert response == CreateOrderResponseModel(**mock_response)
        mock_exec_request.assert_called_once_with(
            client.RequestMethod.POST,
            client._order_url,
            payload.model_dump(exclude_none=True)
        )

    @pytest.mark.asyncio
    async def test_del_order(self, client, mock_exec_request):
        mock_response = {"data": {"clientId": "clientId", "transactionId": 2}}
        mock_exec_request.return_value = (mock_response, True)
        params = DelOrderModel(
            **{
                "clientId": "clientId", "transactionId": 1
            }
        )
        response = await client.del_order(params)
        assert response == DelOrderResponseModel(**mock_response)
        mock_exec_request.assert_called_once_with(
            client.RequestMethod.DELETE,
            client._order_url,
            params=params.model_dump()
        )
