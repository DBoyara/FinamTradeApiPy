from enum import Enum

from pydantic import BaseModel


class BaseErrorModel(BaseModel):
    code: str
    message: str
    data: dict | None = None


class ErrorBodyModel(BaseModel):
    error: BaseErrorModel


class Market(str, Enum):
    Stock = "Stock"
    Forts = "Forts"
    Spbex = "Spbex"
    Mma = "Mma"
    Ets = "Ets"
    Bonds = "Bonds"
    Options = "Options"
