import asyncio
from abc import ABC
from datetime import datetime, timedelta
from enum import Enum
from typing import TYPE_CHECKING, Any

import httpx

from .token_manager import TokenManager

if TYPE_CHECKING:
    from finam_trade_api.access.access_token import TokenClient


class BaseClient(ABC):
    """
    Базовый клиент для выполнения HTTP-запросов с использованием токенов аутентификации.

    Атрибуты:
        _token_manager (TokenManager): Менеджер токенов для управления JWT-токеном.
        _base_url (str): Базовый URL для всех запросов.
        _token_client (TokenClient | None): Клиент для обновления JWT токена.
        _last_token_refresh (datetime | None): Время последнего обновления токена.
        _token_refresh_interval (timedelta): Интервал обновления токена (по умолчанию 10 минут).
        _refresh_lock (asyncio.Lock): Блокировка для предотвращения одновременного обновления токена.
    """

    class RequestMethod(str, Enum):
        """
        Перечисление методов HTTP-запросов.
        """
        POST = "post"
        PUT = "put"
        GET = "get"
        DELETE = "delete"

    def __init__(self, token_manager: TokenManager, url: str = "https://api.finam.ru/v1"):
        """
        Инициализирует экземпляр BaseClient.

        Параметры:
            token_manager (TokenManager): Экземпляр менеджера токенов.
            url (str): Базовый URL для запросов. По умолчанию "https://api.finam.ru/v1".
        """
        self._token_manager = token_manager
        self._base_url = url
        self._token_client: "TokenClient | None" = None
        self._last_token_refresh: datetime | None = None
        self._token_refresh_interval = timedelta(minutes=10)
        self._refresh_lock = asyncio.Lock()

    def set_token_client(self, token_client: "TokenClient"):
        """
        Устанавливает клиент для обновления токенов.

        Параметры:
            token_client (TokenClient): Экземпляр TokenClient для обновления JWT токена.
        """
        self._token_client = token_client

    @property
    def _auth_headers(self):
        """
        Генерирует заголовки аутентификации для запросов.

        Возвращает:
            dict | None: Словарь с заголовком Authorization, если JWT-токен установлен, иначе None.
        """
        return {"Authorization": self._token_manager.jwt_token} if self._token_manager.jwt_token else None

    def _should_refresh_token(self) -> bool:
        """
        Проверяет, нужно ли обновить токен по таймеру.

        Возвращает:
            bool: True, если токен нужно обновить, иначе False.
        """
        if self._last_token_refresh is None:
            return True
        return datetime.now() - self._last_token_refresh >= self._token_refresh_interval

    async def _refresh_token(self):
        """
        Обновляет JWT токен.

        Использует блокировку для предотвращения одновременного обновления токена
        из нескольких запросов.
        """
        async with self._refresh_lock:
            if self._last_token_refresh is not None:
                if datetime.now() - self._last_token_refresh < timedelta(seconds=5):
                    return

            if self._token_client is not None:
                await self._token_client.set_jwt_token()
                self._last_token_refresh = datetime.now()

    async def _exec_request(self, method: str, url: str, payload=None, **kwargs) -> tuple[Any, bool]:
        """
        Выполняет HTTP-запрос к указанному URL.

        Автоматически обновляет JWT токен при получении ошибки авторизации (401)
        или если прошло более 10 минут с последнего обновления.

        Параметры:
            method (str): HTTP-метод (GET, POST, PUT, DELETE).
            url (str): Путь к ресурсу относительно базового URL.
            payload (dict | None): Тело запроса в формате JSON. По умолчанию None.
            **kwargs: Дополнительные параметры для aiohttp.

        Возвращает:
            tuple[Any, bool]: Кортеж, содержащий JSON-ответ и статус успешности запроса (True/False).

        Исключения:
            httpx.HTTPError: Если статус ответа не 200 и content_type не "application/json".
        """
        if self._token_client is not None and self._should_refresh_token():
            await self._refresh_token()

        uri = f"{self._base_url}{url}"

        async with httpx.AsyncClient(headers=self._auth_headers, http2=True) as client:
            response = await client.request(method, uri, json=payload, **kwargs)

            if response.status_code == 401 and self._token_client is not None:
                await self._refresh_token()

                async with httpx.AsyncClient(headers=self._auth_headers, http2=True) as retry_client:
                    response = await retry_client.request(method, uri, json=payload, **kwargs)

            if response.status_code != 200:
                if "application/json" not in response.headers.get("content-type", ""):
                    response.raise_for_status()
                return response.json(), False
            return response.json(), True
