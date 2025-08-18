
# FinamTradeApiPy

[![Build](https://github.com/Dboyara/FinamTradeApiPy/actions/workflows/py-checks.yaml/badge.svg)](https://github.com/Dboyara/FinamTradeApiPy/actions/workflows/py-checks.yaml)
[![PyPI version](https://badge.fury.io/py/finam-trade-api.svg)](https://pypi.org/project/finam-trade-api/)
![Python](https://img.shields.io/pypi/pyversions/finam-trade-api)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com/)
![License](https://img.shields.io/github/license/Dboyara/FinamTradeApiPy)
![Code style: Ruff](https://img.shields.io/badge/code%20style-ruff-informational?logo=python&logoColor=white)
![Type Checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)
![Formatted with: black](https://img.shields.io/badge/format-black-black)
![Security Check](https://img.shields.io/badge/security-passed-brightgreen)
![GitHub stars](https://img.shields.io/github/stars/Dboyara/FinamTradeApiPy?style=social)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/DBoyara/FinamTradeApiPy)

---

FinamTradeApiPy — это Python-библиотека для лёгкого взаимодействия с публичным торговым API Finam.
Библиотека только предоставляет удобную обертку для доступа к API и не несет ответственность за полученные и отправленные через нее данные.

# Обновление FinamApi !!!

Так как Finam переезжает на новое API, библиотека будет обновляться.
Версия будет начинаться с 4.х.х и уже доступна в [PyPi](https://pypi.org/project/finam-trade-api/4.0.1/).
Предыдущая версия остановилась на [3.1.2](https://github.com/DBoyara/FinamTradeApiPy/releases/tag/3.1.2) и доступна в PyPi.
В нее больше изменения вноситься не будут.

Асинхронный REST-клиент для API [Finam](https://tradeapi.finam.ru/docs/about/).

Используется:
1. [aiohttp](https://github.com/aio-libs/aiohttp) для создания клиента;
2. [pydantic](https://github.com/pydantic/pydantic) для удобной работы с моделями данных;
3. [ruff](https://github.com/astral-sh/ruff) для линтинга;
4. [mypy](https://github.com/python/mypy) для статической типизации;
5. [pytest](https://github.com/pytest-dev/pytest) для тестирования;
6. [bandit](https://github.com/PyCQA/bandit) для статического анализа безопасности;
7. [pre-commit](https://github.com/pre-commit/pre-commit) для автоматизации линтинга и тестирования;

## Requirements
Python >= 3.11; < 3.14 - проверки в CI.

## Installation

```bash
pip install finam-trade-api
poetry add finam-trade-api
```
    
## Usage/Examples

### Получение токена

```python
import os

from finam_trade_api import Client
from finam_trade_api import TokenManager


async def main():
    # Получение токена из переменных окружения
    token = os.getenv("TOKEN")
    
    # Инициализация клиента с менеджером токенов
    client = Client(TokenManager(token))
    
    # Установка JWT-токена
    await client.access_tokens.set_jwt_token()
    
    # Получение деталей JWT-токена
    return await client.access_tokens.get_jwt_token_details()


if __name__ == "__main__":
    import asyncio

    # Запуск асинхронного main
    print(asyncio.run(main()))
```

### Информация об аккаунте

```python
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

    # Получение информации об аккаунте
    pprint(await client.account.get_account_info(account_id))

    # Получение списка транзакций
    pprint(await client.account.get_transactions(GetTransactionsRequest(
        account_id=account_id,
        start_time="2024-01-01T00:00:00Z",
        end_time="2025-03-15T00:00:00Z",
        limit=10,
    )))

    # Получение списка сделок
    pprint(await client.account.get_trades(GetTradesRequest(
        account_id=account_id,
        start_time="2024-01-01T00:00:00Z",
        end_time="2025-03-15T00:00:00Z",
    )))


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### Больше примеров в папке [examples](https://github.com/DBoyara/FinamTradeApiPy/tree/master/examples)

## Authors

- [@DBoyara](https://www.github.com/DBoyara)


## License

[GNU GPL v.3.0](https://choosealicense.com/licenses/gpl-3.0/)

