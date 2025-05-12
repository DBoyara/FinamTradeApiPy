from enum import Enum

from pydantic import BaseModel, Field


class ErrorModel(BaseModel):
    code: int
    message: str
    details: list = Field(default_factory=list)


class ErrorBodyModel(BaseModel):
    # todo remove it
    error: dict


class Market(str, Enum):
    Stock = "Stock"
    Forts = "Forts"
    Spbex = "Spbex"
    Mma = "Mma"
    Ets = "Ets"
    Bonds = "Bonds"
    Options = "Options"
