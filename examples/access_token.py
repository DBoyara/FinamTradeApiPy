import os

from finam.client import Client


async def main():
    client = Client(os.getenv("TOKEN"))
    return await client.access_tokens.check_token()


if __name__ == "__main__":
    import asyncio

    print(asyncio.run(main()))
