from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel


class OrderType(str, Enum):
    Sell = "Sell"
    Buy = "Buy"


class ConditionType(str, Enum):
    Bid = "Bid"
    BidOrLast = "BidOrLast"
    Ask = "Ask"
    AskOrLast = "AskOrLast"
    CovDown = "CovDown"
    CovUp = "CovUp"
    LastUp = "LastUp"
    LastDown = "LastDown"


class PropertyType(str, Enum):
    PutInQueue = "PutInQueue"
    CancelBalance = "CancelBalance"
    ImmOrCancel = "ImmOrCancel"


class ValidBeforeType(str, Enum):
    TillEndSession = "TillEndSession"
    TillCancelled = "TillCancelled"
    ExactTime = "ExactTime"


class OrdersRequestModel(BaseModel):
    clientId: str
    includeMatched: Optional[str] = None
    includeCanceled: Optional[str] = None
    includeActive: Optional[str] = None


class Condition(BaseModel):
    type: str
    price: float
    time: str


class ValidateBefore(BaseModel):
    type: ValidBeforeType
    time: str


class OrderResponse(BaseModel):
    orderNo: int
    transactionId: int
    securityCode: str
    clientId: str
    status: Any
    buySell: OrderType
    createdAt: str
    acceptedAt: Optional[str] = None
    price: float
    quantity: int
    balance: int
    message: str
    currency: str
    condition: Optional[Condition] = None
    validateBefore: Optional[ValidateBefore] = None


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
    board: str
    securityCode: str
    buySell: OrderType
    quantity: int
    useCredit: bool = False
    price: Optional[float]
    property: PropertyType
    condition: Optional[Condition] = None
    validateBefore: Optional[ValidateBefore] = None


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
