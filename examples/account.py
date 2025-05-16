import os
from pprint import pprint

from finam_trade_api import Client
from finam_trade_api import TokenManager
from finam_trade_api.account import GetTransactionsRequest, GetTradesRequest

token = os.getenv("TOKEN")
account_id = os.getenv("ACCOUNT_ID")


async def main():
    client = Client(TokenManager(token))
    await client.access_tokens.set_jwt_token()

    pprint(await client.account.get_account_info(account_id))

    pprint(await client.account.get_transactions(GetTransactionsRequest(
        account_id=account_id,
        start_time="2024-01-01T00:00:00Z",
        end_time="2025-03-15T00:00:00Z",
        limit=10,
    )))

    pprint(await client.account.get_trades(GetTradesRequest(
        account_id=account_id,
        start_time="2024-01-01T00:00:00Z",
        end_time="2025-03-15T00:00:00Z",
    )))


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
