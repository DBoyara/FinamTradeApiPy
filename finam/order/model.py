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
    includeActive: str = "true"


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
    price: float = 0
    property: PropertyType = PropertyType.PutInQueue.value
    condition: Optional[Condition] = None
    validateBefore: Optional[ValidateBefore] = None


class DelOrderModel(BaseModel):
    clientId: str
    transactionId: int


class DelOrderResponseModel(BaseModel):
    data: DelOrderModel
