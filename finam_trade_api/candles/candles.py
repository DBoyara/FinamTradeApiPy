from typing import List

from finam_trade_api.base_client import BaseClient
from finam_trade_api.candles.model import (
    DayCandle,
    DayCandlesRequestModel,
    DayCandlesResponse,
    IntraDayCandle,
    IntraDayCandlesRequestModel,
    IntraDayCandlesResponse
)
from finam_trade_api.exceptions import FinamTradeApiError
from finam_trade_api.models import ErrorBodyModel


class CandlesClient(BaseClient):
    def __init__(self, token: str):
        super().__init__(token)
        self._day_url = "/api/v1/day-candles"
        self._in_day_url = "/api/v1/intraday-candles"

    async def get_day_candles(self, params: DayCandlesRequestModel) -> List[DayCandle]:
        p = {
            "securityBoard": params.securityBoard,
            "securityCode": params.securityCode,
            "timeFrame": params.timeFrame.value,
            "interval.From": params.intervalFrom,
            "interval.To": params.intervalTo,
            "interval.Count": params.count,
        }

        response, ok = await self._exec_request(
            self.RequestMethod.GET,
            self._day_url,
            params={k: v for k, v in p.items() if v is not None},
        )
        if not ok:
            err = ErrorBodyModel(**response)
            raise FinamTradeApiError(f"{err.error.code} | {err.error.data} | {err.error.message}")
        return DayCandlesResponse(**response).data.candles

    async def get_in_day_candles(self, params: IntraDayCandlesRequestModel) -> List[IntraDayCandle]:
        p = {
            "securityBoard": params.securityBoard,
            "securityCode": params.securityCode,
            "timeFrame": params.timeFrame.value,
            "interval.From": params.intervalFrom,
            "interval.To": params.intervalTo,
            "interval.Count": params.count,
        }

        response, ok = await self._exec_request(
            self.RequestMethod.GET,
            self._in_day_url,
            params={k: v for k, v in p.items() if v is not None},
        )
        if not ok:
            err = ErrorBodyModel(**response)
            raise FinamTradeApiError(f"{err.error.code} | {err.error.data} | {err.error.message}")
        return IntraDayCandlesResponse(**response).data.candles
