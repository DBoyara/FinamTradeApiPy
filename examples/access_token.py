from finam_trade_api import Client
from finam_trade_api.base_client.token_manager import TokenManager


async def main():
    token = "token сгенерированный на https://tradeapi.finam.ru/docs/tokens"

    client = Client(TokenManager(token))

    await client.access_tokens.set_jwt_token()

    return await client.access_tokens.get_jwt_token_details()


if __name__ == "__main__":
    import asyncio

    print(asyncio.run(main()))
