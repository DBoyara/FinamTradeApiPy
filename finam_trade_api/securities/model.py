from typing import List

from pydantic import BaseModel


class Security(BaseModel):
    code: str
    board: str
    market: str
    decimals: float
    lotSize: float
    minStep: float
    currency: str
    instrumentCode: str
    shortName: str
    properties: float
    timeZoneName: str
    bpCost: float
    accruedInterest: float
    priceSign: str
    ticker: str
    lotDivider: float


class SecurityData(BaseModel):
    securities: List[Security]


class SecurityResponseModel(BaseModel):
    data: SecurityData
