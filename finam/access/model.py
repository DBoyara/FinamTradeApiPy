from pydantic import BaseModel


class TokenData(BaseModel):
    id: int


class TokenResponseModel(BaseModel):
    data: TokenData
