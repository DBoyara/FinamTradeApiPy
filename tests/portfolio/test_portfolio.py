from unittest.mock import AsyncMock, patch

import pytest

from finam_trade_api.exceptions import FinamTradeApiError
from finam_trade_api.models import ErrorBodyModel
from finam_trade_api.portfolio.model import PortfolioRequestModel, PortfolioResponseModel
from finam_trade_api.portfolio.portfolio import PortfolioClient


class TestPortfolioClient:

    @pytest.fixture
    def client(self):
        return PortfolioClient(token="dummy_token")

    @pytest.fixture
    def request_params(self):
        return PortfolioRequestModel(
            clientId="123",
            includeCurrencies="true",
            includeMoney="true",
            includePositions="true",
            includeMaxBuySell="true"
        )

    @pytest.fixture
    def successful_response(self):
        return {
            "data": {
                "clientId": "123",
                "content": {
                    "includeCurrencies": True,
                    "includeMoney": True,
                    "includePositions": True,
                    "includeMaxBuySell": True,
                },
                "equity": 10.10,
                "balance": 1000,
                "currencies": [],
                "money": [],
                "positions": [],
            }
        }

    @pytest.fixture
    def error_response(self):
        return {
            "error": {
                "code": "400",
                "data": None,
                "message": "Bad Request"
            }
        }

    @patch('finam_trade_api.portfolio.portfolio.PortfolioClient._exec_request', new_callable=AsyncMock)
    @pytest.mark.asyncio
    async def test_get_portfolio_success(self, mock_exec_request, client, request_params, successful_response):
        mock_exec_request.return_value = (successful_response, True)
        response = await client.get_portfolio(request_params)
        assert isinstance(response, PortfolioResponseModel)
        assert response.data.clientId == "123"

    @patch('finam_trade_api.portfolio.portfolio.PortfolioClient._exec_request', new_callable=AsyncMock)
    @pytest.mark.asyncio
    async def test_get_portfolio_error(self, mock_exec_request, client, request_params, error_response):
        mock_exec_request.return_value = (error_response, False)
        with pytest.raises(FinamTradeApiError) as exc_info:
            await client.get_portfolio(request_params)
        assert "400 | None | Bad Request" in str(exc_info.value)
