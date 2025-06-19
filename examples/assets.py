import os
from pprint import pprint
import asyncio

from finam_trade_api import Client, TokenManager

token = os.getenv("TOKEN")
underlying_symbol = "YDEX@RTSX"
instrument_symbol = "YDEX@MISX"

async def main():
    client = Client(TokenManager(token))
    await client.access_tokens.set_jwt_token()

    pprint(await client.assets.get_exchanges())

    pprint(await client.assets.get_options_chain(underlying_symbol))

    pprint(await client.assets.get_schedule(instrument_symbol))

    try:
        await client.assets.get_assets()
    except NotImplementedError as e:
        print("Метод get_assets не реализован:", e)

    pprint(await client.assets.get_asset(instrument_symbol, "1346867"))

    await client.assets.get_asset_params(instrument_symbol, "1346867")


if __name__ == "__main__":
    asyncio.run(main())