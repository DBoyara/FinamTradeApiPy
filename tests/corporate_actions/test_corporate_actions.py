import pytest
from unittest.mock import AsyncMock, patch

from finam_trade_api.base_client.models import FinamDate
from finam_trade_api.corporate_actions.corporate_actions import CorporateActionsClient
from finam_trade_api.corporate_actions.model import BondsEventsResponse, SortDirection
from finam_trade_api.exceptions import FinamTradeApiError


@pytest.fixture
def token_manager():
    tm = AsyncMock()
    tm.token = "valid_token"
    return tm


@pytest.fixture
def corporate_actions_client(token_manager):
    return CorporateActionsClient(token_manager)


# ---- get_future_bonds_events ----


@pytest.mark.asyncio
async def test_get_future_bonds_events_success(corporate_actions_client):
    response_data = {
        "symbol": "SU26238RMFS5",
        "pagination": {"total": 1, "limit": 10, "offset": 0, "has_next": False},
        "events": [
            {
                "date": {"year": 2026, "month": 9, "day": 15},
                "type": "COUPON",
                "value": {"value": "12.50"},
                "currency": "RUB",
                "coupon_details": {
                    "record_date": {"year": 2026, "month": 9, "day": 10},
                    "start_date": {"year": 2026, "month": 3, "day": 15},
                    "face_value": {"value": "1000.00"},
                    "value_percent": {"value": "7.50"},
                },
            }
        ],
    }
    with patch.object(
        corporate_actions_client, "_exec_request", return_value=(response_data, True)
    ) as mock_exec:
        result = await corporate_actions_client.get_future_bonds_events()
        mock_exec.assert_called_once_with(
            corporate_actions_client.RequestMethod.GET, "/bonds/future", params={}
        )
        assert isinstance(result, BondsEventsResponse)
        assert result.symbol == "SU26238RMFS5"
        assert len(result.events) == 1
        assert result.events[0].date.year == 2026
        assert result.events[0].type == "COUPON"
        assert result.pagination.total == 1
        assert result.pagination.has_next is False


@pytest.mark.asyncio
async def test_get_future_bonds_events_failure(corporate_actions_client):
    error_response = {"code": 401, "message": "Unauthorized", "details": []}
    with patch.object(
        corporate_actions_client, "_exec_request", return_value=(error_response, False)
    ) as mock_exec:
        with pytest.raises(FinamTradeApiError, match="code=401 | message=Unauthorized"):
            await corporate_actions_client.get_future_bonds_events()
        mock_exec.assert_called_once()


@pytest.mark.asyncio
async def test_get_future_bonds_events_with_params(corporate_actions_client):
    response_data = {
        "symbol": "SU26238RMFS5",
        "pagination": {"total": 0, "limit": 5, "offset": 10, "has_next": True},
        "events": [],
    }
    date_from = FinamDate(year=2026, month=1, day=1)
    date_to = FinamDate(year=2026, month=12, day=31)

    with patch.object(
        corporate_actions_client, "_exec_request", return_value=(response_data, True)
    ) as mock_exec:
        result = await corporate_actions_client.get_future_bonds_events(
            symbol="SU26238RMFS5",
            date_from=date_from,
            date_to=date_to,
            sort_direction=SortDirection.ASC,
            limit=5,
            offset=10,
        )
        mock_exec.assert_called_once_with(
            corporate_actions_client.RequestMethod.GET,
            "/bonds/future",
            params={
                "symbol": "SU26238RMFS5",
                "date_from.year": 2026,
                "date_from.month": 1,
                "date_from.day": 1,
                "date_to.year": 2026,
                "date_to.month": 12,
                "date_to.day": 31,
                "sort_direction": "ASC",
                "limit": 5,
                "offset": 10,
            },
        )
        assert isinstance(result, BondsEventsResponse)
        assert result.pagination.has_next is True


# ---- get_past_bonds_events ----


@pytest.mark.asyncio
async def test_get_past_bonds_events_success(corporate_actions_client):
    response_data = {
        "symbol": "SU26238RMFS5",
        "pagination": {"total": 2, "limit": 10, "offset": 0, "has_next": False},
        "events": [
            {
                "date": {"year": 2026, "month": 3, "day": 15},
                "type": "COUPON",
                "value": {"value": "12.50"},
                "currency": "RUB",
            },
            {
                "date": {"year": 2025, "month": 9, "day": 15},
                "type": "COUPON",
                "value": {"value": "12.50"},
                "currency": "RUB",
            },
        ],
    }
    with patch.object(
        corporate_actions_client, "_exec_request", return_value=(response_data, True)
    ) as mock_exec:
        result = await corporate_actions_client.get_past_bonds_events()
        mock_exec.assert_called_once_with(
            corporate_actions_client.RequestMethod.GET, "/bonds/past", params={}
        )
        assert isinstance(result, BondsEventsResponse)
        assert result.symbol == "SU26238RMFS5"
        assert len(result.events) == 2
        assert result.pagination.total == 2


@pytest.mark.asyncio
async def test_get_past_bonds_events_failure(corporate_actions_client):
    error_response = {"code": 500, "message": "Internal Error", "details": []}
    with patch.object(
        corporate_actions_client, "_exec_request", return_value=(error_response, False)
    ) as mock_exec:
        with pytest.raises(FinamTradeApiError, match="code=500 | message=Internal Error"):
            await corporate_actions_client.get_past_bonds_events()
        mock_exec.assert_called_once()


@pytest.mark.asyncio
async def test_get_past_bonds_events_with_params(corporate_actions_client):
    response_data = {
        "symbol": "SU26238RMFS5",
        "pagination": {"total": 0, "limit": 5, "offset": 0, "has_next": False},
        "events": [],
    }
    date_from = FinamDate(year=2025, month=1, day=1)

    with patch.object(
        corporate_actions_client, "_exec_request", return_value=(response_data, True)
    ) as mock_exec:
        result = await corporate_actions_client.get_past_bonds_events(
            symbol="SU26238RMFS5",
            date_from=date_from,
            sort_direction=SortDirection.DESC,
            limit=5,
        )
        mock_exec.assert_called_once_with(
            corporate_actions_client.RequestMethod.GET,
            "/bonds/past",
            params={
                "symbol": "SU26238RMFS5",
                "date_from.year": 2025,
                "date_from.month": 1,
                "date_from.day": 1,
                "sort_direction": "DESC",
                "limit": 5,
            },
        )
        assert isinstance(result, BondsEventsResponse)
