from enum import Enum

from pydantic import BaseModel


class DayInterval(str, Enum):
    D1 = "D1"
    W1 = "W1"


class IntraDayInterval(str, Enum):
    M1 = "M1"
    M5 = "M5"
    M15 = "M15"
    H1 = "H1"


class BaseCandlesRequestModel(BaseModel):
    securityBoard: str
    securityCode: str
    intervalFrom: str | None = None
    intervalTo: str | None
    count: int | None


class DayCandlesRequestModel(BaseCandlesRequestModel):
    timeFrame: DayInterval


class IntraDayCandlesRequestModel(BaseCandlesRequestModel):
    timeFrame: IntraDayInterval


class Decimal(BaseModel):
    num: int
    scale: int


class BaseCandleModel(BaseModel):
    open: Decimal
    close: Decimal
    high: Decimal
    low: Decimal
    volume: int


class DayCandle(BaseCandleModel):
    date: str


class CandlesResponse(BaseModel):
    candles: list[DayCandle]


class DayCandlesResponse(BaseModel):
    data: CandlesResponse


class IntraDayCandle(BaseCandleModel):
    timestamp: str


class InDayCandlesResponse(BaseModel):
    candles: list[IntraDayCandle]


class IntraDayCandlesResponse(BaseModel):
    data: InDayCandlesResponse
