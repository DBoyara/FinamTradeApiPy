from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from finam_trade_api.base_client.models import FinamDecimal, Side


class OrderStatus(str, Enum):
    """Статус заявки"""
    UNSPECIFIED = "ORDER_STATUS_UNSPECIFIED"
    NEW = "ORDER_STATUS_NEW"
    PARTIALLY_FILLED = "ORDER_STATUS_PARTIALLY_FILLED"
    FILLED = "ORDER_STATUS_FILLED"
    DONE_FOR_DAY = "ORDER_STATUS_DONE_FOR_DAY"
    CANCELED = "ORDER_STATUS_CANCELED"
    REPLACED = "ORDER_STATUS_REPLACED"
    PENDING_CANCEL = "ORDER_STATUS_PENDING_CANCEL"
    REJECTED = "ORDER_STATUS_REJECTED"
    SUSPENDED = "ORDER_STATUS_SUSPENDED"
    PENDING_NEW = "ORDER_STATUS_PENDING_NEW"
    EXPIRED = "ORDER_STATUS_EXPIRED"
    FAILED = "ORDER_STATUS_FAILED"
    FORWARDING = "ORDER_STATUS_FORWARDING"
    WAIT = "ORDER_STATUS_WAIT"
    DENIED_BY_BROKER = "ORDER_STATUS_DENIED_BY_BROKER"
    REJECTED_BY_EXCHANGE = "ORDER_STATUS_REJECTED_BY_EXCHANGE"
    WATCHING = "ORDER_STATUS_WATCHING"
    EXECUTED = "ORDER_STATUS_EXECUTED"
    DISABLED = "ORDER_STATUS_DISABLED"
    LINK_WAIT = "ORDER_STATUS_LINK_WAIT"
    SL_GUARD_TIME = "ORDER_STATUS_SL_GUARD_TIME"
    SL_EXECUTED = "ORDER_STATUS_SL_EXECUTED"
    SL_FORWARDING = "ORDER_STATUS_SL_FORWARDING"
    TP_GUARD_TIME = "ORDER_STATUS_TP_GUARD_TIME"
    TP_EXECUTED = "ORDER_STATUS_TP_EXECUTED"
    TP_CORRECTION = "ORDER_STATUS_TP_CORRECTION"
    TP_FORWARDING = "ORDER_STATUS_TP_FORWARDING"
    TP_CORR_GUARD_TIME = "ORDER_STATUS_TP_CORR_GUARD_TIME"


class OrderType(str, Enum):
    """Тип заявки"""
    UNSPECIFIED = "ORDER_TYPE_UNSPECIFIED"
    MARKET = "ORDER_TYPE_MARKET"
    LIMIT = "ORDER_TYPE_LIMIT"
    STOP = "ORDER_TYPE_STOP"
    STOP_LIMIT = "ORDER_TYPE_STOP_LIMIT"
    MULTI_LEG = "ORDER_TYPE_MULTI_LEG"


class StopCondition(str, Enum):
    """Условие срабатывания стоп заявки"""
    UNSPECIFIED = "STOP_CONDITION_UNSPECIFIED"
    LAST_UP = "STOP_CONDITION_LAST_UP"
    LAST_DOWN = "STOP_CONDITION_LAST_DOWN"


class TimeInForce(str, Enum):
    """Срок действия заявки"""
    UNSPECIFIED = "TIME_IN_FORCE_UNSPECIFIED"
    DAY = "TIME_IN_FORCE_DAY"
    GOOD_TILL_CANCEL = "TIME_IN_FORCE_GOOD_TILL_CANCEL"
    GOOD_TILL_CROSSING = "TIME_IN_FORCE_GOOD_TILL_CROSSING"
    EXT = "TIME_IN_FORCE_EXT"
    ON_OPEN = "TIME_IN_FORCE_ON_OPEN"
    ON_CLOSE = "TIME_IN_FORCE_ON_CLOSE"
    IOC = "TIME_IN_FORCE_IOC"
    FOK = "TIME_IN_FORCE_FOK"


class ValidBefore(str, Enum):
    """Срок действия условной заявки"""
    UNSPECIFIED = "VALID_BEFORE_UNSPECIFIED"
    END_OF_DAY = "VALID_BEFORE_END_OF_DAY"
    GOOD_TILL_CANCEL = "VALID_BEFORE_GOOD_TILL_CANCEL"
    GOOD_TILL_DATE = "VALID_BEFORE_GOOD_TILL_DATE"


class Leg(BaseModel):
    """Лег"""
    symbol: str
    quantity: FinamDecimal
    side: Side


class Order(BaseModel):
    """Информация о заявке"""
    account_id: str
    symbol: str
    quantity: FinamDecimal
    side: Side
    type: OrderType
    time_in_force: TimeInForce | None = None
    limit_price: FinamDecimal | str | None = None
    stop_price: FinamDecimal | str | None = None
    stop_condition: StopCondition | None = None
    legs: list[Leg] = Field(default_factory=list)
    client_order_id: str | None = Field(default=None, max_length=64)
    valid_before: ValidBefore | None = None
    comment: str | None = Field(default=None, max_length=128)


class CancelOrderRequest(BaseModel):
    """Запрос отмены торговой заявки"""
    account_id: str
    order_id: str


class GetOrderRequest(BaseModel):
    """Запрос на получение конкретного ордера"""
    account_id: str
    order_id: str


class OrdersRequest(BaseModel):
    """Запрос получения списка торговых заявок"""
    account_id: str


class OrderState(BaseModel):
    """Состояние заявки"""
    order_id: str
    exec_id: str
    status: OrderStatus
    order: Order
    transact_at: datetime
    accept_at: datetime | None = None
    withdraw_at: datetime | None = None
    initial_quantity: FinamDecimal | str | None = None
    executed_quantity: FinamDecimal | str | None = None
    remaining_quantity: FinamDecimal | str | None = None


class OrdersResponse(BaseModel):
    """Список торговых заявок"""
    orders: list[OrderState]
