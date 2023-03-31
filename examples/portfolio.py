import os

from finam_trade_api.client import Client
from finam_trade_api.portfolio.model import PortfolioRequestModel

token = os.getenv("TOKEN")
client_id = os.getenv("CLIENT_ID")


async def main():
    client = Client(token)
    params = PortfolioRequestModel(clientId=client_id)
    return await client.portfolio.get_portfolio(params)


if __name__ == "__main__":
    import asyncio

    print(asyncio.run(main()))
