from enum import Enum

from pydantic import BaseModel

from finam_trade_api.models import Market


class OrderType(str, Enum):
    Sell = "Sell"
    Buy = "Buy"


class ConditionType(str, Enum):
    Bid = "Bid"  # лучшая цена покупки
    BidOrLast = "BidOrLast"  # лучшая цена покупки или сделка по заданной цене и выше
    Ask = "Ask"  # лучшая цена продажи
    AskOrLast = "AskOrLast"  # лучшая цена продажи или сделка по заданной цене и ниже
    CovDown = "CovDown"  # обеспеченность ниже заданной
    CovUp = "CovUp"  # обеспеченность выше заданной
    LastUp = "LastUp"  # сделка на рынке по заданной цене или выше
    LastDown = "LastDown"  # сделка на рынке по заданной цене или ниже


class PropertyType(str, Enum):
    PutInQueue = "PutInQueue"  # неисполненная часть заявки помещается в очередь заявок биржи;
    CancelBalance = "CancelBalance"  # неисполненная часть заявки снимается с торгов;
    ImmOrCancel = "ImmOrCancel"  # сделки совершаются в том случае, если заявка может быть удовлетворена полностью


class ValidBeforeType(str, Enum):
    TillEndSession = "TillEndSession"  # до конца дня
    TillCancelled = "TillCancelled"  # до отмены
    ExactTime = "ExactTime"  # до указанной даты


class BoardType(str, Enum):
    Futures = "FUT"
    ZLG = "ZLG"
    TQBR = "TQBR"
    TQTF = "TQTF"


class StopQuantityUnits(str, Enum):
    Percent = "Percent"
    Lots = "Lots"


class StopPriceUnits(str, Enum):
    Percent = "Percent"
    Pips = "Pips"


class OrdersRequestModel(BaseModel):
    clientId: str
    includeMatched: str | None = None
    includeCanceled: str | None = None
    includeActive: str | None = None


class Condition(BaseModel):
    type: ConditionType
    price: float  # цена активации
    time: str | None = None


class ValidBefore(BaseModel):
    type: ValidBeforeType
    time: str | None = None


class OrderStatus(str, Enum):
    NONE = "None"
    Active = "Active"
    Cancelled = "Cancelled"
    Matched = "Matched"


class StopQuantity(BaseModel):
    value: float  # Значение объема.
    units: StopQuantityUnits  # Единицы объема стоп-заявки.


class StopLossModel(BaseModel):
    activationPrice: float
    price: float | None = None
    marketPrice: bool
    quantity: StopQuantity
    time: int = 0  # Защитное время, сек.
    useCredit: bool = False


class StopPrice(BaseModel):
    value: float  # Значение объема.
    units: StopPriceUnits  # Единицы объема стоп-заявки.


class TakeProfitModel(BaseModel):
    activationPrice: float
    correctionPrice: StopPrice | None = None
    spreadPrice: StopPrice | None = None
    marketPrice: bool
    quantity: StopQuantity
    time: int = 0  # Защитное время, сек.
    useCredit: bool = False

class Order(BaseModel):
    orderNo: int
    transactionId: int
    securityCode: str | None = None
    clientId: str | None = None
    status: OrderStatus
    buySell: OrderType
    createdAt: str | None = None
    acceptedAt: str | None = None
    price: float | None = None
    quantity: int
    balance: int
    message: str | None = None
    currency: str | None = None
    condition: Condition | None = None
    validBefore: ValidBefore | None = None
    securityBoard: str | None = None
    market: Market


class OrdersResponseData(BaseModel):
    clientId: str
    orders: list[Order]


class OrdersResponseModel(BaseModel):
    data: OrdersResponseData


class StopOrder(BaseModel):
    stopId: int
    securityCode: str
    securityBoard: BoardType
    market: Market
    clientId: str
    buySell: OrderType
    expirationDate: str | None = None
    linkOrder: int
    validBefore: ValidBefore | None = None
    status: OrderStatus
    message: str | None = None
    orderNo: int
    tradeNo: int
    acceptedAt: str | None = None
    canceledAt: str | None = None
    currency: str | None = None
    takeProfitExtremum: float
    takeProfitLevel: float
    stopLoss: StopLossModel | None = None
    takeProfit: TakeProfitModel | None = None


class StopOrdersResponseData(BaseModel):
    clientId: str
    stops: list[StopOrder]


class StopOrdersResponseModel(BaseModel):
    data: StopOrdersResponseData


class CreatedOrder(BaseModel):
    clientId: str
    transactionId: int
    securityCode: str


class CreateOrderResponseModel(BaseModel):
    data: CreatedOrder


class CreateOrderRequestModel(BaseModel):
    clientId: str
    securityBoard: BoardType
    securityCode: str
    buySell: OrderType
    quantity: int
    useCredit: bool = False
    price: float | None = None
    property: PropertyType
    condition: Condition | None = None
    validBefore: ValidBefore | None = None


class CreateStopOrderRequestModel(BaseModel):
    clientId: str
    securityBoard: BoardType
    securityCode: str
    buySell: OrderType
    stopLoss: StopLossModel
    takeProfit: TakeProfitModel
    expirationDate: str | None = None
    linkOrder: int | None = None
    validBefore: ValidBefore | None = None


class CreateStopOrderData(BaseModel):
    clientId: str
    stopId: int
    securityCode: str | None = None
    securityBoard: str | None = None


class CreateStopOrderResponseModel(BaseModel):
    data: CreateStopOrderData


class DelOrderModel(BaseModel):
    clientId: str
    transactionId: int


class DelOrderResponseModel(BaseModel):
    data: DelOrderModel


class DelStopOrderRequestModel(BaseModel):
    clientId: str
    stopOrderId: int


class DelStopOrderData(BaseModel):
    clientId: str
    stopOrderId: int


class DelStopOrderResponseModel(BaseModel):
    data: DelStopOrderData
