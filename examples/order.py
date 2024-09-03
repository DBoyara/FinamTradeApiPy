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
    TakeProfitModel,
)

token = os.getenv("TOKEN", "")
client_id = os.getenv("CLIENT_ID", "")
client = Client(token)


async def create_order():
    payload = CreateOrderRequestModel(
        clientId=client_id,
        securityBoard=BoardType.TQBR,
        securityCode="ALRS",
        buySell=OrderType.Buy,
        quantity=1,
        price=72.23,
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


async def del_order(transaction_id: int):
    params = DelOrderModel(
        clientId=client_id,
        transactionId=transaction_id
    )
    return await client.orders.del_order(params)


async def create_stop_order(transaction_id: int):
    payload = CreateStopOrderRequestModel(
        clientId=client_id,
        securityBoard=BoardType.TQBR,
        securityCode="ALRS",
        buySell=OrderType.Sell,
        linkOrder=transaction_id,
        stopLoss=StopLossModel(
            activationPrice=71.80,
            marketPrice=True,
            quantity=StopQuantity(
                value=1,
                units=StopQuantityUnits.Lots,
            )
        ),
        takeProfit=TakeProfitModel(
            activationPrice=72.30,
            marketPrice=True,
            quantity=StopQuantity(
                value=1,
                units=StopQuantityUnits.Lots,
            )
        ),
    )
    return await client.orders.create_stop_order(payload)
