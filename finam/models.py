from pydantic import BaseModel


class ErrorBodyModel(BaseModel):
    code: str
    message: str
    data: dict


class BaseErrorModel(BaseModel):
    error: ErrorBodyModel
