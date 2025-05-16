import os
from pprint import pprint

from finam_trade_api import Client
from finam_trade_api import TokenManager
from finam_trade_api.instruments.model import BarsRequest, TimeFrame

token = os.getenv("TOKEN")


async def main():
    client = Client(TokenManager(token))
    await client.access_tokens.set_jwt_token()

    params = BarsRequest(
        symbol="YDEX@MISX",
        start_time="2025-03-01T00:00:00Z",
        end_time="2025-03-15T00:00:00Z",
        timeframe=TimeFrame.TIME_FRAME_D,
    )
    pprint(await client.instruments.get_bars(params))

    pprint(await client.instruments.get_last_quote("YDEX@MISX"))

    pprint(await client.instruments.get_last_trades("YDEX@MISX"))

    pprint(await client.instruments.get_order_book("YDEX@MISX"))


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
