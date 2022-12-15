import os

from finam.client import Client

token = os.getenv("TOKEN", "")
client = Client(token)


async def get_all_data():
    return await client.securities.get_data()


async def get_data_by_code(code: str):
    return await client.securities.get_data(code)


if __name__ == "__main__":
    import asyncio

    print(asyncio.run(get_all_data()))

    code_ = "SiZ2"
    print(asyncio.run(get_data_by_code(code_)))
