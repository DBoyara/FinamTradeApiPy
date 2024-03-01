from typing import List, Optional

from pydantic import BaseModel

from finam_trade_api.models import Market


class Security(BaseModel):
    code: str
    board: str
    market: Market
    decimals: int
    lotSize: int
    minStep: int
    currency: Optional[str] = None
    shortName: Optional[str] = None
    properties: int
    timeZoneName: Optional[str] = None
    bpCost: float
    accruedInterest: float
    priceSign: str
    ticker: Optional[str] = None
    lotDivider: int


class SecurityData(BaseModel):
    securities: List[Security]


class SecurityResponseModel(BaseModel):
    data: SecurityData
