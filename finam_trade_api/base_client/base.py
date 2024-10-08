from abc import ABC
from enum import Enum
from typing import Any, Tuple

import aiohttp


class BaseClient(ABC):
    class RequestMethod(str, Enum):
        POST = "post"
        PUT = "put"
        GET = "get"
        DELETE = "delete"

    def __init__(self, token: str, url: str = "https://trade-api.finam.ru"):
        self._token = token
        self._base_url = url

    @property
    def _auth_headers(self):
        return {"X-Api-Key": self._token}

    async def _exec_request(self, method: str, url: str, payload=None, **kwargs) -> Tuple[Any, bool]:
        uri = f"{self._base_url}{url}"

        async with aiohttp.ClientSession(headers=self._auth_headers) as session:
            async with session.request(method, uri, json=payload, **kwargs) as response:
                if response.status != 200:
                    if response.content_type != "application/json":
                        response.raise_for_status()
                    return await response.json(), False
                return await response.json(), True
