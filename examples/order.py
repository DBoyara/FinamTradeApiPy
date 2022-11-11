import os

from finam.client import Client
from finam.order.model import (
    BoardType,
    CreateOrderRequestModel,
    DelOrderModel,
    OrdersRequestModel,
    OrderType,
    PropertyType,
)

token = os.getenv("TOKEN", "")
client_id = os.getenv("CLIENT_ID")
client = Client(token)


async def create_order():
    payload = CreateOrderRequestModel(
        clientId=client_id,
        board=BoardType.Futures,
        securityCode="SiZ2",
        buySell=OrderType.Buy,
        quantity=1,
        price=60000,
        property=PropertyType.PutInQueue,
        condition=None,
        validateBefore=None,
    )
    return await client.orders.create_order(payload)


async def get_orders():
    params = OrdersRequestModel(
        client_id=client_id,
        includeActive="true"
    )
    return await client.orders.get_orders(params)


async def del_order(transaction_id: str):
    params = DelOrderModel(
        client_id=client_id,
        transactionId=transaction_id
    )
    return await client.orders.del_order(params)


if __name__ == "__main__":
    import asyncio

    res = asyncio.run(create_order())
    print(res)

    print(asyncio.run(get_orders()))

    print(asyncio.run(del_order(res.data.transactionId)))

    print(asyncio.run(get_orders()))
