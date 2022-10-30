from typing import Any

from pydantic import BaseModel

from finam.models import BaseErrorModel


class PortfolioRequestOptionalModel(BaseModel):
    includeCurrencies: bool = False
    includeMoney: bool = False
    includePositions: bool = False
    includeMaxBuySell: bool = False


class PortfolioRequestModel(PortfolioRequestOptionalModel):
    client_id: str


class PortfolioResponseData(BaseModel):
    clientId: str
    content: PortfolioRequestOptionalModel
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
