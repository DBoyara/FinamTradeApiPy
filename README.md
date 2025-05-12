
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

---

FinamTradeApiPy — это Python-библиотека для лёгкого взаимодействия с публичным торговым API Finam.

## 📦 Установка

```bash
pip install finam-trade-api-py
poetry add finam-trade-api

# Обновление FinamApi !!!

Так как Finam переезжает на новое API, библиотека будет обновляться. Происходить это будет по мере появления методов REST-Api.
Версия будет начинаться с 4.х.х-beta 

Асинхронный REST-клиент для API [Finam](https://finamweb.github.io/trade-api-docs).

Используется [aiohttp](https://github.com/aio-libs/aiohttp) для создания клиента и [pydantic](https://github.com/pydantic/pydantic) для удобной работы с моделями данных.


## Requirements
Python >= 3.11

## Documentation

[Документация Trade-Api](https://trade-api.finam.ru/swagger/index.html)


## Installation

Install with pip

```bash
  pip install finam-trade-api
```
    
## Usage/Examples

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

## Authors

- [@DBoyara](https://www.github.com/DBoyara)


## License

[GNU GPL v.3.0](https://choosealicense.com/licenses/gpl-3.0/)

