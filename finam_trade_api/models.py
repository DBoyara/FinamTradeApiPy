from typing import Optional

from pydantic import BaseModel


class BaseErrorModel(BaseModel):
    code: str
    message: str
    data: Optional[dict]


class ErrorBodyModel(BaseModel):
    error: BaseErrorModel
