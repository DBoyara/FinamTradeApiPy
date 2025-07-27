from datetime import datetime

from pydantic import BaseModel, Field

from finam_trade_api.base_client.models import FinamDecimal, FinamMoney


class Position(BaseModel):
    symbol: str
    quantity: FinamDecimal
    average_price: FinamDecimal
    current_price: FinamDecimal


class GetAccountResponse(BaseModel):
    account_id: str
    type: str
    status: str
    equity: FinamDecimal
    unrealized_profit: FinamDecimal
    positions: list[Position] = Field(default_factory=list)
    cash: list[FinamMoney] = Field(default_factory=list)


class GetTransactionsRequest(BaseModel):
    account_id: str
    start_time: str
    end_time: str
    limit: int = 10


class GetTradesRequest(GetTransactionsRequest):
    ...


class Trade(BaseModel):
    size: FinamDecimal
    price: FinamDecimal
    accrued_interest: FinamDecimal


class Transaction(BaseModel):
    id: str
    category: str
    timestamp: str
    symbol: str
    change: FinamMoney | None = None
    trade: Trade | None = None


class GetTransactionsResponse(BaseModel):
    transactions: list[Transaction]


class AccountTrade(BaseModel):
    trade_id: str
    symbol: str
    price: FinamDecimal
    size: FinamDecimal
    side: str
    timestamp: datetime


class GetTradesResponse(BaseModel):
    trades: list[AccountTrade]
