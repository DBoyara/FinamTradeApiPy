import asyncio

from finam_trade_api import Client, TokenManager
from finam_trade_api.base_client.models import FinamDate
from finam_trade_api.corporate_actions import SortDirection

tm = TokenManager(secret="your-secret")
client = Client(tm)

async def main():
    # Будущие события по облигации
    events = await client.corporate_actions.get_future_bonds_events(
        symbol="SU26238RMFS5",
        limit=10,
    )

    # Исторические события с фильтром по дате
    events = await client.corporate_actions.get_past_bonds_events(
        date_from=FinamDate(year=2025, month=1, day=1),
        date_to=FinamDate(year=2025, month=12, day=31),
        sort_direction=SortDirection.DESC,
    )


if __name__ == "__main__":
    asyncio.run(main())
