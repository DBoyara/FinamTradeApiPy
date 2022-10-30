from abc import ABC
from enum import Enum

import aiohttp


class BaseClient(ABC):
    class RequestMethod(str, Enum):
        POST = "post"
        PUT = "put"
        GET = "get"
        DELETE = "delete"

    def __init__(self, token: str):
        self._token = token
        self._base_url = "https://trade-api.comon.ru"

    def _get_auth_headers(self):
        return {"Authorization": f"Bearer {self._token}"}

    async def _exec_request(self, method: str, url: str, payload=None, **kwargs):
        headers = self._get_auth_headers()
        uri = f"{self._base_url}/{url}"

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.request(method, uri, json=payload, **kwargs) as response:
                if response.status != 200:
                    return response.json()

                if response.content_type == "application/json":
                    return await response.json()
                return await response.text()
