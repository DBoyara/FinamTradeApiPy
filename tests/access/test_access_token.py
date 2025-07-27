from datetime import datetime

import pytest
from unittest.mock import AsyncMock, patch

from finam_trade_api.access import TokenClient
from finam_trade_api.exceptions import FinamTradeApiError
from finam_trade_api.access.model import TokenDetailsResponse


@pytest.mark.asyncio
async def test_sets_jwt_token_on_successful_response():
    token_manager = AsyncMock()
    token_manager.token = "valid_secret"  # pragma: allowlist secret
    client = TokenClient(token_manager)

    with patch.object(client, "_exec_request", return_value=({"token": "jwt_token"}, True)) as mock_request:
        await client.set_jwt_token()
        mock_request.assert_called_once_with(
            client.RequestMethod.POST,
            "/sessions",
            payload={"secret": "valid_secret"},
        )
        token_manager.set_jwt_token.assert_called_once_with("jwt_token")


@pytest.mark.asyncio
async def test_raises_error_on_failed_jwt_token_request():
    token_manager = AsyncMock()
    token_manager.token = "invalid_secret"  # pragma: allowlist secret
    client = TokenClient(token_manager)

    error_response = {"code": 401, "message": "Unauthorized", "details": []}
    with patch.object(client, "_exec_request", return_value=(error_response, False)):
        with pytest.raises(FinamTradeApiError, match="code=401 | message=Unauthorized | details=Invalid secret"):
            await client.set_jwt_token()


@pytest.mark.asyncio
async def test_returns_token_details_on_successful_request():
    token_manager = AsyncMock()
    token_manager.jwt_token = "valid_jwt_token"  # pragma: allowlist secret
    client = TokenClient(token_manager)

    token_details = {
        "created_at": datetime.now(),
        "expires_at": datetime.now(),
        "account_ids": ["1"],
        "md_permissions": [{"quote_level": "quoteLevel", "delay_minutes": 0, "mic": "mic"}]
    }
    with patch.object(client, "_exec_request", return_value=(token_details, True)):
        result = await client.get_jwt_token_details()
        assert isinstance(result, TokenDetailsResponse)
        assert result.created_at
        assert result.expires_at
        assert result.account_ids and "1" in result.account_ids
