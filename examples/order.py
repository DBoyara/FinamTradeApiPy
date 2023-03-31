import os

from finam_trade_api.client import Client
from finam_trade_api.order.model import (
    BoardType,
    CreateOrderRequestModel,
    CreateStopOrderRequestModel,
    DelOrderModel,
    OrdersRequestModel,
    OrderType,
    PropertyType,
    StopLossModel,
    StopQuantity,
    StopQuantityUnits,
    TakeProfitModel
)

token = os.getenv("TOKEN", "")
client_id = os.getenv("CLIENT_ID", "")
client = Client(token)


async def create_order():
    payload = CreateOrderRequestModel(
        clientId=client_id,
        securityBoard=BoardType.Futures,
        securityCode="SiH3",
        buySell=OrderType.Sell,
        quantity=1,
        price=74920,
        property=PropertyType.PutInQueue,
        condition=None,
        validateBefore=None,
    )
    return await client.orders.create_order(payload)


async def get_orders():
    params = OrdersRequestModel(
        clientId=client_id,
        includeActive="true",
        includeMatched="true",
    )
    return await client.orders.get_orders(params)


async def del_order(transaction_id: str):
    params = DelOrderModel(
        client_id=client_id,
        transactionId=transaction_id
    )
    return await client.orders.del_order(params)


async def create_stop_order(transaction_id: int):
    payload = CreateStopOrderRequestModel(
        clientId=client_id,
        securityBoard=BoardType.Futures,
        securityCode="SiH3",
        buySell=OrderType.Buy,
        linkOrder=transaction_id,
        stopLoss=StopLossModel(
            activationPrice=74940,
            marketPrice=True,
            quantity=StopQuantity(
                value=1,
                units=StopQuantityUnits.Lots,
            )
        ),
        takeProfit=TakeProfitModel(
            activationPrice=74850,
            marketPrice=True,
            quantity=StopQuantity(
                value=1,
                units=StopQuantityUnits.Lots,
            )
        ),
    )
    return await client.orders.create_stop_order(payload)


if __name__ == "__main__":
    import asyncio

    res = asyncio.run(create_order())
    print(res)

    print(asyncio.run(create_stop_order(1111111111111111111)))

    print(asyncio.run(get_orders()))

    print(asyncio.run(del_order(res.data.transactionId)))

    print(asyncio.run(get_orders()))
