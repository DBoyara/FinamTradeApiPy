from pydantic import BaseModel

from finam_trade_api.models import Market


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
    market: Market
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
    positions: list[Position]
    currencies: list[Currency]
    money: list[Money]


class PortfolioResponseModel(BaseModel):
    data: PortfolioResponseData
