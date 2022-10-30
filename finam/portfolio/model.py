from typing import Any

from pydantic import BaseModel, Field

from finam.models import BaseErrorModel


class PortfolioRequestOptionalModel(BaseModel):
    include_currencies: bool = Field(False, alias='Content.IncludeCurrencies')
    include_money: bool = Field(False, alias='Content.IncludeMoney')
    include_positions: bool = Field(False, alias='Content.IncludePositions')
    include_maxBuySell: bool = Field(False, alias='Content.IncludeMaxBuySell')


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
