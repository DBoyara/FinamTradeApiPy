from datetime import datetime

from pydantic import BaseModel

from finam_trade_api.base_client.models import FinamDate, FinamDecimal


class Exchange(BaseModel):
    mic: str
    name: str


class ExchangesResponse(BaseModel):
    exchanges: list[Exchange]


class Option(BaseModel):
    symbol: str
    type: str
    contractSize: FinamDecimal
    tradeFirstDay: FinamDate | None = None
    tradeLastDay: FinamDate
    strike: FinamDecimal
    multiplier: FinamDecimal | None = None


class OptionsChainResponse(BaseModel):
    symbol: str
    options: list[Option]


class SessionInterval(BaseModel):
    startTime: datetime
    endTime: datetime


class Session(BaseModel):
    type: str
    interval: SessionInterval


class ScheduleResponse(BaseModel):
    symbol: str
    sessions: list[Session]
