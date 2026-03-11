"""
Пример демонстрирующий автоматическое обновление JWT токена.

Клиент автоматически обновляет JWT токен в двух случаях:
1. При получении ошибки авторизации (401) от API
2. Каждые 10 минут (превентивное обновление)

Это позволяет избежать ошибок авторизации при длительной работе с API.
"""

import asyncio
from finam_trade_api import Client
from finam_trade_api.base_client.token_manager import TokenManager


async def main():
    # Токен сгенерированный на https://tradeapi.finam.ru/docs/tokens
    token = "your_secret_token_here"

    # Создаем клиент
    client = Client(TokenManager(token))

    # Получаем первичный JWT токен
    await client.access_tokens.set_jwt_token()
    print("JWT токен успешно получен")

    # Проверяем детали токена
    token_details = await client.access_tokens.get_jwt_token_details()
    print(f"Детали токена: {token_details}")

    # Теперь можно использовать любые методы API
    # JWT токен будет автоматически обновляться:
    # - При получении ошибки 401
    # - Каждые 10 минут

    # Пример: получаем список счетов
    accounts = await client.account.get_accounts()
    print(f"Получены счета: {accounts}")

    # Можно работать длительное время без ручного обновления токена
    # Например, запросить данные несколько раз с задержкой
    for i in range(3):
        print(f"\nЗапрос {i + 1}:")
        accounts = await client.account.get_accounts()
        print(f"Счетов: {len(accounts.accounts) if hasattr(accounts, 'accounts') else 0}")

        # Задержка между запросами
        if i < 2:
            await asyncio.sleep(5)

    print("\nВсе запросы выполнены успешно!")
    print("JWT токен автоматически обновлялся при необходимости")


if __name__ == "__main__":
    asyncio.run(main())
