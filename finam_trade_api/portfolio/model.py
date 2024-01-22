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
    currentPrice: float
    equity: float
    averagePrice: float
    currency: str
    accumulatedProfit: float
    todayProfit: float
    unrealizedProfit: float
    profit: float
    maxBuy: int
    maxSell: int
    priceCurrency: str
    averagePriceCurrency: str
    averageRate: float


class Currency(BaseModel):
    name: str
    balance: float
    crossRate: float
    equity: float
    unrealizedProfit: float


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
