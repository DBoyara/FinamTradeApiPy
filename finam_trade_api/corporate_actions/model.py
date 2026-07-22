from enum import StrEnum

from pydantic import BaseModel

from finam_trade_api.base_client.models import FinamDate, FinamDecimal


class SortDirection(StrEnum):
    """Направление сортировки по дате."""
    ASC = "ASC"
    DESC = "DESC"


class BondEventType(StrEnum):
    """Тип события по облигации."""
    UNSPECIFIED = "UNSPECIFIED"


class CouponDetails(BaseModel):
    """Детали купонного платежа."""
    record_date: FinamDate | None = None
    start_date: FinamDate | None = None
    face_value: FinamDecimal | None = None
    value_percent: FinamDecimal | None = None


class AmortizationDetails(BaseModel):
    """Детали амортизации облигации."""
    new_face_value: FinamDecimal | None = None
    initial_face_value: FinamDecimal | None = None
    amortization_percent: FinamDecimal | None = None


class OfferDetails(BaseModel):
    """Детали оффера по облигации."""
    offer_type: str | None = None
    price: FinamDecimal | None = None
    start_date: FinamDate | None = None
    end_date: FinamDate | None = None
    agent: str | None = None


class BondEvent(BaseModel):
    """Событие по облигации."""
    date: FinamDate
    type: BondEventType | str = BondEventType.UNSPECIFIED
    value: FinamDecimal | None = None
    currency: str | None = None
    coupon_details: CouponDetails | None = None
    amortization_details: AmortizationDetails | None = None
    offer_details: OfferDetails | None = None


class Pagination(BaseModel):
    """Параметры пагинации ответа."""
    total: int
    limit: int
    offset: int
    has_next: bool


class BondsEventsResponse(BaseModel):
    """Ответ API на запрос событий по облигациям."""
    symbol: str
    pagination: Pagination
    events: list[BondEvent]
