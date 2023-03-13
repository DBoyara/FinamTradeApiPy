from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


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
    PutInQueue = "PutInQueue"
    CancelBalance = "CancelBalance"
    ImmOrCancel = "ImmOrCancel"


class ValidBeforeType(str, Enum):
    TillEndSession = "TillEndSession"  # до конца дня
    TillCancelled = "TillCancelled"  # до отмены
    ExactTime = "ExactTime"  # до указанной даты


class BoardType(str, Enum):
    Futures = "FUT"
    ZLG = "ZLG"
    TQBR = "TQBR"


class StopQuantityUnits(str, Enum):
    Percent = "Percent"
    Lots = "Lots"


class StopPriceUnits(str, Enum):
    Percent = "Percent"
    Pips = "Pips"


class OrdersRequestModel(BaseModel):
    clientId: str
    includeMatched: Optional[str] = None
    includeCanceled: Optional[str] = None
    includeActive: Optional[str] = None


class Condition(BaseModel):
    type: ConditionType
    price: float  # цена активации
    time: Optional[str] = None


class ValidBefore(BaseModel):
    type: ValidBeforeType
    time: Optional[str] = None


class OrderStatus(str, Enum):
    Active = "Active"
    Cancelled = "Cancelled"
    Matched = "Matched"


class OrderResponse(BaseModel):
    orderNo: int
    transactionId: int
    securityCode: Optional[str] = None
    clientId: Optional[str] = None
    status: Optional[OrderStatus] = None
    buySell: OrderType
    createdAt: Optional[str] = None
    acceptedAt: Optional[str] = None
    price: float = 0
    quantity: int
    balance: int
    message: Optional[str] = None
    currency: Optional[str] = None
    condition: Optional[Condition] = None
    validBefore: Optional[ValidBefore] = None


class OrdersResponseData(BaseModel):
    clientId: str
    orders: List[OrderResponse]


class OrdersResponseModel(BaseModel):
    data: OrdersResponseData


class StopOrder(BaseModel):
    stopOrderId: int
    securityCode: str


class StopOrdersResponseData(BaseModel):
    clientId: str
    stopOrders: List[StopOrder]


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
    price: Optional[float]  # цена заявки
    property: PropertyType
    condition: Optional[Condition] = None
    validBefore: Optional[ValidBefore] = None


class StopQuantity(BaseModel):
    value: float  # Значение объема.
    units: StopQuantityUnits  # Единицы объема стоп-заявки.


class StopLossModel(BaseModel):
    activationPrice: float
    price: Optional[float] = None
    marketPrice: bool
    quantity: StopQuantity


class StopPrice(BaseModel):
    value: float  # Значение объема.
    units: StopPriceUnits  # Единицы объема стоп-заявки.


class TakeProfitModel(BaseModel):
    activationPrice: float
    correctionPrice: Optional[StopPrice] = None
    spreadPrice: Optional[StopPrice] = None
    marketPrice: bool
    quantity: StopQuantity
    time: Optional[int] = None  # Защитное время, сек.
    useCredit: bool = False


class CreateStopOrderRequestModel(BaseModel):
    clientId: str
    securityBoard: BoardType
    securityCode: str
    buySell: OrderType
    stopLoss: StopLossModel
    takeProfit: TakeProfitModel
    expirationDate: Optional[str] = None
    linkOrder: Optional[int] = None
    validBefore: Optional[ValidBefore] = None


class CreateStopOrderData(BaseModel):
    clientId: str
    stopId: int
    securityCode: Optional[str] = None
    securityBoard: Optional[str] = None


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
