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
