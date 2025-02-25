import os

from finam_trade_api.candles.model import (
    DayCandlesRequestModel,
    DayInterval,
    IntraDayCandlesRequestModel,
    IntraDayInterval,
)
from finam_trade_api.client import Client

token = os.getenv("TOKEN", "CAEQx4uXBhoY976DzzTuCEu0XXVtJ76bj2kvUAhgvX2a")


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
        securityBoard="FUT",
        securityCode="CRH5",
        timeFrame=IntraDayInterval.M5,
        intervalTo='2025-02-24 14:25:45',
        count=10
    )
    return await client.candles.get_in_day_candles(params)


if __name__ == "__main__":
    import asyncio

    # print(asyncio.run(get_day_candles()))

    print(asyncio.run(get_in_day_candles()))
