from datetime import datetime

from pydantic import BaseModel, Field

from finam_trade_api.base_client.models import FinamDecimal


class Position(BaseModel):
    symbol: str
    quantity: FinamDecimal
    averagePrice: FinamDecimal
    currentPrice: FinamDecimal


class GetAccountResponse(BaseModel):
    accountId: str
    type: str
    status: str
    equity: FinamDecimal
    unrealizedProfit: FinamDecimal
    positions: list[Position] = Field(default_factory=list)
    cash: list = Field(default_factory=list)  # todo не задокументировано


class GetTransactionsRequest(BaseModel):
    account_id: str
    start_time: str
    end_time: str
    limit: int = 10


class GetTradesRequest(GetTransactionsRequest):
    ...


class MoneyChange(BaseModel):
    currencyCode: str
    units: str
    nanos: int


class Trade(BaseModel):
    size: FinamDecimal
    price: FinamDecimal
    accruedInterest: FinamDecimal


class Transaction(BaseModel):
    id: str
    category: str
    timestamp: str
    symbol: str
    change: MoneyChange | None = None
    trade: Trade | None = None


class GetTransactionsResponse(BaseModel):
    transactions: list[Transaction]


class AccountTrade(BaseModel):
    tradeId: str
    symbol: str
    price: FinamDecimal
    size: FinamDecimal
    side: str
    timestamp: datetime


class GetTradesResponse(BaseModel):
    trades: list[AccountTrade]
