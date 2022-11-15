from typing import List

from pydantic import BaseModel


class PortfolioRequestOptionalModel(BaseModel):
    includeCurrencies: str = "true"
    includeMoney: str = "false"
    includeMaxBuySell: str = "true"
    includePositions: str = "true"


class PortfolioRequestModel(PortfolioRequestOptionalModel):
    clientId: str


class PortfolioContent(BaseModel):
    includeCurrencies: bool
    includeMoney: bool
    includePositions: bool
    includeMaxBuySell: bool


class Position(BaseModel):
    securityCode: str
    market: str
    balance: int
    currentPrice: int
    equity: int
    averagePrice: int
    currency: str
    accumulatedProfit: int
    todayProfit: int
    unrealizedProfit: int
    profit: int
    maxBuy: int
    maxSell: int
    priceCurrency: str
    averagePriceCurrency: str
    averageRate: int


class Currency(BaseModel):
    name: str
    balance: float
    crossRate: int
    equity: float
    unrealizedProfit: int


class Money(BaseModel):
    market: str
    currency: str
    balance: float


class PortfolioResponseData(BaseModel):
    clientId: str
    content: PortfolioContent
    equity: float
    balance: float
    positions: List[Position]
    currencies: List[Currency]
    money: List[Money]


class PortfolioResponseModel(BaseModel):
    data: PortfolioResponseData
