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
    contract_size: FinamDecimal
    trade_first_day: FinamDate | None = None
    trade_last_day: FinamDate
    strike: FinamDecimal
    multiplier: FinamDecimal | None = None


class OptionsChainResponse(BaseModel):
    symbol: str
    options: list[Option]


class SessionInterval(BaseModel):
    start_time: datetime
    end_time: datetime


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
    min_step: str
    lot_size: FinamDecimal
    expiration_date: str | None = None


class Status(BaseModel):
    value: str
    halted_days: int = 0


class AssetParamsResponse(BaseModel):
    symbol: str
    account_id: str
    tradeable: bool
    longable: Status
    shortable: Status
    long_risk_rate: FinamDecimal | None = None
    long_collateral: FinamMoney | None = None
    short_risk_rate: FinamDecimal | None = None
    short_collateral: FinamMoney | None = None


class ClockResponse(BaseModel):
    timestamp: datetime
