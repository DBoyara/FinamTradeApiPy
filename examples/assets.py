import os
from pprint import pprint
import asyncio

from finam_trade_api import Client, TokenManager

token = os.getenv("TOKEN")
account_id = os.getenv("ACCOUNT_ID")
instrument_symbol = "YDEX@MISX"

async def main():
    client = Client(TokenManager(token))
    await client.access_tokens.set_jwt_token()

    pprint(await client.assets.get_assets())

    pprint(await client.assets.get_exchanges())

    pprint(await client.assets.get_options_chain(instrument_symbol))

    pprint(await client.assets.get_schedule(instrument_symbol))

    pprint(await client.assets.get_asset(instrument_symbol, account_id))

    pprint(await client.assets.get_asset_params(instrument_symbol, account_id))

    pprint(await client.assets.get_clock())


if __name__ == "__main__":
    asyncio.run(main())
