class TokenManager:
    """
    Класс для управления токенами, включая основной токен и JWT-токен.

    Атрибуты:
        _token (str): Основной токен, передаваемый при инициализации.
        _jwt_token (str | None): JWT-токен, который может быть установлен позже.
    """

    def __init__(self, token: str):
        """
        Инициализирует экземпляр TokenManager с основным токеном.

        Параметры:
            token (str): Основной токен, используемый для аутентификации.
        """
        self._token = token
        self._jwt_token: str | None = None

    @property
    def token(self) -> str:
        """
        Возвращает основной токен.

        Возвращает:
            str: Основной токен.
        """
        return self._token

    @property
    def jwt_token(self) -> str | None:
        """
        Возвращает текущий JWT-токен.

        Возвращает:
            str | None: JWT-токен, если он установлен, иначе None.
        """
        return self._jwt_token

    def set_jwt_token(self, jwt_token: str):
        """
        Устанавливает значение JWT-токена.

        Параметры:
            jwt_token (str): Новый JWT-токен.
        """
        self._jwt_token = jwt_token
