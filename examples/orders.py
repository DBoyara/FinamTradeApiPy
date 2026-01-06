import os
from pprint import pprint

from finam_trade_api import Client
from finam_trade_api import TokenManager
from finam_trade_api.base_client import FinamDecimal
from finam_trade_api.base_client.models import Side
from finam_trade_api.order import OrdersRequest, GetOrderRequest, Order, OrderType, TimeInForce

token = os.getenv("TOKEN")

account_id = os.getenv("ACCOUNT_ID")

async def main():
    client = Client(TokenManager(token))
    await client.access_tokens.set_jwt_token()

    params = OrdersRequest(account_id=account_id)
    pprint(await client.orders.get_orders(params))

    params = GetOrderRequest(account_id=account_id, order_id="")
    pprint(await client.orders.get_order(params))

    pprint(await client.orders.cancel_order(params))

    order = Order(
        account_id=account_id,
        symbol="SBER@MISX",
        quantity=FinamDecimal(value="1"),
        side=Side.BUY,
        type=OrderType.LIMIT,
        time_in_force=TimeInForce.DAY,
        limit_price=FinamDecimal(value="290.0"),
    )
    pprint(await client.orders.place_order(order))

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
