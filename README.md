
# FinamTradeApiPy

Асинхронный клиент для API Finam: https://trade-api.comon.ru и их сервиса https://comon.ru

Используется [aiohttp](https://github.com/aio-libs/aiohttp) для создания клиента и [pydantic](https://github.com/pydantic/pydantic) для удобной работы с моделями данных.


## Documentation

[Документация Trade-Api](https://trade-api.comon.ru/swagger/index.html)


## Installation

Install with pip

```bash
  pip install finam-trade-api
```
    
## Usage/Examples

### Получение информации об инструменте

```python
import os

from finam.client import Client

token = os.getenv("TOKEN")
client_id = os.getenv("CLIENT_ID")
client = Client(token)


async def get_all_data():
    return await client.securities.get_data()


async def get_data_by_code(code: str):
    return await client.securities.get_data(code)


if __name__ == '__main__':
    import asyncio

    print(asyncio.run(get_all_data()))

    code_ = "SiZ2"
    print(asyncio.run(get_data_by_code(code_)))
```

### Получение информации об портфеле

```python
import os

from finam.client import Client
from finam.portfolio.model import PortfolioRequestModel


token = os.getenv("TOKEN")
client_id = os.getenv("CLIENT_ID")


async def main():
    client = Client(token)
    params = PortfolioRequestModel(clientId=client_id)
    return await client.portfolio.get_portfolio(params)


if __name__ == '__main__':
    import asyncio

    print(asyncio.run(main()))
```

### Работа с заявками

```python
import os

from finam.client import Client
from finam.order.model import (
    BoardType,
    CreateOrderRequestModel,
    CreateStopOrderRequestModel,
    DelOrderModel,
    OrdersRequestModel,
    OrderType,
    PropertyType,
    StopLossModel,
    StopQuantity,
    StopQuantityUnits,
    TakeProfitModel
)

token = os.getenv("TOKEN", "")
client_id = os.getenv("CLIENT_ID", "")
client = Client(token)


async def create_order():
    payload = CreateOrderRequestModel(
        clientId=client_id,
        securityBoard=BoardType.Futures,
        securityCode="SiH3",
        buySell=OrderType.Sell,
        quantity=1,
        price=74920,
        property=PropertyType.PutInQueue,
        condition=None,
        validateBefore=None,
    )
    return await client.orders.create_order(payload)


async def get_orders():
    params = OrdersRequestModel(
        clientId=client_id,
        includeActive="true",
        includeMatched="true",
    )
    return await client.orders.get_orders(params)


async def del_order(transaction_id: str):
    params = DelOrderModel(
        client_id=client_id,
        transactionId=transaction_id
    )
    return await client.orders.del_order(params)


async def create_stop_order(transaction_id: int):
    payload = CreateStopOrderRequestModel(
        clientId=client_id,
        securityBoard=BoardType.Futures,
        securityCode="SiH3",
        buySell=OrderType.Buy,
        linkOrder=transaction_id,
        stopLoss=StopLossModel(
            activationPrice=74940,
            marketPrice=True,
            quantity=StopQuantity(
                value=1,
                units=StopQuantityUnits.Lots,
            )
        ),
        takeProfit=TakeProfitModel(
            activationPrice=74850,
            marketPrice=True,
            quantity=StopQuantity(
                value=1,
                units=StopQuantityUnits.Lots,
            )
        ),
    )
    return await client.orders.create_stop_order(payload)


if __name__ == "__main__":
    import asyncio

    res = asyncio.run(create_order())
    print(res)

    print(asyncio.run(create_stop_order(1111111111111111111)))

    print(asyncio.run(get_orders()))

    print(asyncio.run(del_order(res.data.transactionId)))

    print(asyncio.run(get_orders()))
```


## Features

- Поддержать proto-историю с events

## Authors

- [@DBoyara](https://www.github.com/DBoyara)


## License

[GNU GPL v.3.0](https://choosealicense.com/licenses/gpl-3.0/)

