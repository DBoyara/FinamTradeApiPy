from pydantic import BaseModel, Field


class FinamDecimal(BaseModel):
    """
    A custom decimal type for Finam API responses.
    """
    value: float = 0.0
