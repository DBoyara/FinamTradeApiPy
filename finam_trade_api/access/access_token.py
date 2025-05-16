from finam_trade_api.access.model import TokenDetailsResponse
from finam_trade_api.base_client import BaseClient
from finam_trade_api.base_client.token_manager import TokenManager
from finam_trade_api.exceptions import FinamTradeApiError
from finam_trade_api.models import ErrorModel


class TokenClient(BaseClient):
    """
    Клиент для работы с токенами аутентификации.

    Наследуется от:
        BaseClient: Базовый клиент для выполнения HTTP-запросов.

    Атрибуты:
        _url (str): Путь к API для работы с токенами.
    """

    def __init__(self, token_manager: TokenManager):
        """
        Инициализирует экземпляр TokenClient.

        Параметры:
            token_manager (TokenManager): Экземпляр менеджера токенов.
        """
        super().__init__(token_manager)
        self._url = "/sessions"

    async def set_jwt_token(self):
        """
        Устанавливает JWT-токен, выполняя запрос к API.

        Выполняет POST-запрос с секретом из TokenManager для получения нового JWT-токена.
        Устанавливает полученный токен в TokenManager.

        Исключения:
            FinamTradeApiError: Если запрос завершился с ошибкой.
        """
        response, ok = await self._exec_request(
            self.RequestMethod.POST,
            self._url,
            payload={"secret": self._token_manager.token},
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(f"code={err.code} | message={err.message} | details={err.details}")

        self._token_manager.set_jwt_token(response["token"])

    async def get_jwt_token_details(self) -> TokenDetailsResponse:
        """
        Получает детали текущего JWT-токена.

        Выполняет POST-запрос с текущим JWT-токеном из TokenManager для получения его деталей.

        Возвращает:
            TokenDetailsResponse: Объект с деталями токена.

        Исключения:
            FinamTradeApiError: Если запрос завершился с ошибкой.
        """
        response, ok = await self._exec_request(
            self.RequestMethod.POST,
            f"{self._url}/details",
            payload={"token": self._token_manager.jwt_token},
        )

        if not ok:
            err = ErrorModel(**response)
            raise FinamTradeApiError(f"code={err.code} | message={err.message} | details={err.details}")

        return TokenDetailsResponse(**response)
