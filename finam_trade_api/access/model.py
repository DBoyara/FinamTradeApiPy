from datetime import datetime

from pydantic import BaseModel


class MDPermission(BaseModel):
    quoteLevel: str
    delayMinutes: int
    mic: str
    country: str | None = None
    continent: str | None = None
    worldwide: bool = False


class TokenDetailsResponse(BaseModel):
    createdAt: datetime
    expiresAt: datetime
    mdPermissions: list[MDPermission]
    accountIds: list[str]
