from pydantic import BaseModel

from finam_trade_api.models import Market


class Security(BaseModel):
    code: str
    board: str
    market: Market
    decimals: int
    lotSize: int
    minStep: int
    currency: str | None = None
    shortName: str | None = None
    properties: int
    timeZoneName: str | None = None
    bpCost: float
    accruedInterest: float
    priceSign: str
    ticker: str | None = None
    lotDivider: int


class SecurityData(BaseModel):
    securities: list[Security]


class SecurityResponseModel(BaseModel):
    data: SecurityData
