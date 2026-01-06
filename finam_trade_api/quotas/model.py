from datetime import datetime

from pydantic import BaseModel


class QuotasUsage(BaseModel):
    name: str
    limit: str
    remaining: str
    reset_time: datetime | None = None


class QuotasResponse(BaseModel):
    quotas: list[QuotasUsage]
