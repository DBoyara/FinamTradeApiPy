import os

from finam_trade_api.client import Client
from finam_trade_api.candles.model import (
    DayCandlesRequestModel,
    DayInterval,
    IntraDayCandlesRequestModel,
    IntraDayInterval
)

token = os.getenv("TOKEN", "")


async def get_day_candles():
    client = Client(token)
    params = DayCandlesRequestModel(
        securityBoard="TQBR",
        securityCode="SBER",
        timeFrame=DayInterval.D1,
        intervalFrom="2023-06-05",
        intervalTo="2023-06-07",
    )
    return await client.candles.get_day_candles(params)


async def get_in_day_candles():
    client = Client(token)
    params = IntraDayCandlesRequestModel(
        securityBoard="TQBR",
        securityCode="SBER",
        timeFrame=IntraDayInterval.M1,
        intervalFrom="2023-06-07 08:33:52",
        count=10
    )
    return await client.candles.get_in_day_candles(params)


if __name__ == "__main__":
    import asyncio

    print(asyncio.run(get_day_candles()))

    print(asyncio.run(get_in_day_candles()))
