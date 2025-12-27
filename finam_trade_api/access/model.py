from datetime import datetime

from pydantic import BaseModel


class MDPermission(BaseModel):
    quote_level: str
    delay_minutes: int
    mic: str
    country: str | None = None
    continent: str | None = None
    worldwide: bool = False


class TokenDetailsResponse(BaseModel):
    created_at: datetime
    expires_at: datetime
    md_permissions: list[MDPermission]
    account_ids: list[str]
    readonly: bool = False
