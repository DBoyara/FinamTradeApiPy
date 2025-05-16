from enum import Enum

from pydantic import BaseModel


class OrderState(BaseModel):
    orderId: str


class OrdersResponse(BaseModel):
    orders: list[OrderState]
