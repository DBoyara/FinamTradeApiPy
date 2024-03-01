from enum import Enum
from typing import Optional

from pydantic import BaseModel


class BaseErrorModel(BaseModel):
    code: str
    message: str
    data: Optional[dict]


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
