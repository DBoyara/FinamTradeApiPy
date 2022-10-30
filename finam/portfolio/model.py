from typing import Any

from pydantic import BaseModel

from finam.models import BaseErrorModel


class PortfolioRequestOptionalModel(BaseModel):
    include_currencies: bool = False
    include_money: bool = False
    include_positions: bool = False
    include_maxBuySell: bool = False


class PortfolioRequestModel(PortfolioRequestOptionalModel):
    client_id: str


class PortfolioContent(BaseModel):
    includeCurrencies: bool
    includeMoney: bool
    includePositions: bool
    includeMaxBuySell: bool


class PortfolioResponseData(BaseModel):
    clientId: str
    content: PortfolioContent
    equity: float
    balance: float
    positions: list = []
    currencies: list = []
    money: list = []


class PortfolioResponseModel(BaseModel):
    data: PortfolioResponseData
    error: Any


class PortfolioErrorModel(BaseErrorModel):
    ...
