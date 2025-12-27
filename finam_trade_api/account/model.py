from datetime import datetime

from pydantic import BaseModel, Field

from finam_trade_api.base_client.models import FinamDecimal, FinamMoney


class Position(BaseModel):
    symbol: str
    quantity: str
    average_price: str
    current_price: str
    maintenance_margin: str
    daily_pnl: str
    unrealized_pnl: str


class GetAccountResponse(BaseModel):
    account_id: str
    type: str
    status: str
    equity: FinamDecimal | str | None = None
    unrealized_profit: FinamDecimal | str | None = None
    positions: list[Position] = Field(default_factory=list)
    cash: list[FinamMoney] = Field(default_factory=list)
    portfolio_mc: dict = Field(default_factory=dict)
    portfolio_mct: dict = Field(default_factory=dict)
    portfolio_forts: dict = Field(default_factory=dict)
    open_account_date: datetime
    first_trade_date: datetime
    first_non_trade_date: datetime


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
    transaction_category: str
    transaction_name: str
    change_qty: str | None = None


class GetTransactionsResponse(BaseModel):
    transactions: list[Transaction]


class AccountTrade(BaseModel):
    trade_id: str
    symbol: str
    price: FinamDecimal
    size: FinamDecimal
    side: str
    timestamp: datetime
    order_id: str
    account_id: str
    comment: str = ""


class GetTradesResponse(BaseModel):
    trades: list[AccountTrade]
