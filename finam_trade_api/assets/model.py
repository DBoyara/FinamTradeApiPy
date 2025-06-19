from datetime import datetime

from pydantic import BaseModel

from finam_trade_api.base_client.models import FinamDate, FinamDecimal, FinamMoney


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


class BaseAssetModel(BaseModel):
    id: str
    ticker: str
    mic: str
    isin: str
    type: str
    name: str


class Asset(BaseAssetModel):
    symbol: str


class AssetsResponse(BaseModel):
    assets: list[Asset]


class AssetResponse(BaseAssetModel):
    board: str
    decimals: int
    minStep: str
    lotSize: FinamDecimal
    expirationDate: str | None = None


class Status(BaseModel):
    value: str
    haltedDays: int = 0


class AssetParamsResponse(BaseModel):
    symbol: str
    accountId: str
    tradeable: bool
    longable: Status
    shortable: Status
    longRiskRate: FinamDecimal | None = None
    longCollateral: FinamMoney | None = None
    shortRiskRate: FinamDecimal | None = None
    shortCollateral: FinamMoney | None = None


class ClockResponse(BaseModel):
    timestamp: datetime
