from pydantic import BaseModel, Field


class FinamDecimal(BaseModel):
    """
    A custom decimal type for Finam API responses.
    """
    value: float = 0.0


class FinamDate(BaseModel):
    """
    A custom date type for Finam API responses.
    """
    year: int
    month: int
    day: int
