from typing import Any

from pydantic import BaseModel

from finam.models import BaseErrorModel


class PortfolioRequestOptionalModel(BaseModel):
    includeCurrencies: str = "true"
    includeMoney: str = "false"
    includePositions: str = "true"
    includeMaxBuySell: str = "true"


class PortfolioRequestModel(PortfolioRequestOptionalModel):
    clientId: str


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
