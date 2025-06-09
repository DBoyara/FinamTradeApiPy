from abc import ABC
from enum import Enum
from typing import Any

import aiohttp

from .token_manager import TokenManager


class BaseClient(ABC):
    """
    Базовый клиент для выполнения HTTP-запросов с использованием токенов аутентификации.

    Атрибуты:
        _token_manager (TokenManager): Менеджер токенов для управления JWT-токеном.
        _base_url (str): Базовый URL для всех запросов.
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

    @property
    def _auth_headers(self):
        """
        Генерирует заголовки аутентификации для запросов.

        Возвращает:
            dict | None: Словарь с заголовком Authorization, если JWT-токен установлен, иначе None.
        """
        return {"Authorization": self._token_manager.jwt_token} if self._token_manager.jwt_token else None

    async def _exec_request(self, method: str, url: str, payload=None, **kwargs) -> tuple[Any, bool]:
        """
        Выполняет HTTP-запрос к указанному URL.

        Параметры:
            method (str): HTTP-метод (GET, POST, PUT, DELETE).
            url (str): Путь к ресурсу относительно базового URL.
            payload (dict | None): Тело запроса в формате JSON. По умолчанию None.
            **kwargs: Дополнительные параметры для aiohttp.

        Возвращает:
            tuple[Any, bool]: Кортеж, содержащий JSON-ответ и статус успешности запроса (True/False).

        Исключения:
            aiohttp.ClientResponseError: Если статус ответа не 200 и content_type не "application/json".
        """
        uri = f"{self._base_url}{url}"

        async with aiohttp.ClientSession(headers=self._auth_headers) as session:
            async with session.request(method, uri, json=payload, **kwargs) as response:
                if response.status != 200:
                    if response.content_type != "application/json":
                        response.raise_for_status()
                    return await response.json(), False
                return await response.json(), True
