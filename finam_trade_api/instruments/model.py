from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from finam_trade_api.base_client.models import FinamDecimal


class OrderBookRowAction(str, Enum):
    ACTION_UNSPECIFIED = "ACTION_UNSPECIFIED"
    ACTION_REMOVE = "ACTION_REMOVE"
    ACTION_ADD = "ACTION_ADD"
    ACTION_UPDATE = "ACTION_UPDATE"


class TimeFrame(str, Enum):
    TIME_FRAME_UNSPECIFIED = "TIME_FRAME_UNSPECIFIED"
    TIME_FRAME_M1 = "TIME_FRAME_M1"
    TIME_FRAME_M5 = "TIME_FRAME_M5"
    TIME_FRAME_M15 = "TIME_FRAME_M15"
    TIME_FRAME_M30 = "TIME_FRAME_M30"
    TIME_FRAME_H1 = "TIME_FRAME_H1"
    TIME_FRAME_H2 = "TIME_FRAME_H2"
    TIME_FRAME_H4 = "TIME_FRAME_H4"
    TIME_FRAME_H8 = "TIME_FRAME_H8"
    TIME_FRAME_D = "TIME_FRAME_D"
    TIME_FRAME_W = "TIME_FRAME_W"
    TIME_FRAME_MN = "TIME_FRAME_MN"
    TIME_FRAME_QR = "TIME_FRAME_QR"


class BarsRequest(BaseModel):
    symbol: str
    start_time: str
    end_time: str
    timeframe: TimeFrame


class BaseResponse(BaseModel):
    symbol: str


class Bar(BaseModel):
    timestamp: datetime
    open: FinamDecimal
    close: FinamDecimal
    high: FinamDecimal
    low: FinamDecimal
    volume: FinamDecimal


class BarsResponse(BaseResponse):
    bars: list[Bar]


class Quote(BaseModel):
    symbol: str | None = None
    timestamp: datetime
    ask: FinamDecimal
    ask_size: FinamDecimal
    bid: FinamDecimal
    bid_size: FinamDecimal
    last: FinamDecimal
    last_size: FinamDecimal
    volume: FinamDecimal
    turnover: FinamDecimal
    open: FinamDecimal
    close: FinamDecimal
    high: FinamDecimal
    low: FinamDecimal
    change: FinamDecimal


class QuoteResponse(BaseResponse):
    quote: Quote


class Trade(BaseModel):
    trade_id: str
    mpid: str = ""
    timestamp: datetime
    price: FinamDecimal
    size: FinamDecimal


class TradesResponse(BaseResponse):
    trades: list[Trade]


class OrderBookRow(BaseModel):
    price: FinamDecimal
    sell_size: FinamDecimal | None = None
    buy_size: FinamDecimal | None = None
    action: OrderBookRowAction
    mpid: str = ""
    timestamp: datetime


class OrderBook(BaseModel):
    rows: list[OrderBookRow]


class OrderBookResponse(BaseResponse):
    orderbook: OrderBook
