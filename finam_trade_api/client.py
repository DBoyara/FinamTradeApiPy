from finam_trade_api.access import TokenClient
from finam_trade_api.account import AccountClient
from finam_trade_api.assets import AssetsClient
from finam_trade_api.base_client.token_manager import TokenManager
from finam_trade_api.instruments import InstrumentClient
from finam_trade_api.order import OrderClient
from finam_trade_api.quotas import QuotasClient


class Client:
    """
    Главный клиент для работы с Finam Trade API.

    Настраивает обновление JWT токенов для всех подклиентов при auto_refresh_tokens=True.

    Атрибуты:
        account (AccountClient): Клиент для работы со счетами.
        assets (AssetsClient): Клиент для работы с активами.
        orders (OrderClient): Клиент для работы с заявками.
        access_tokens (TokenClient): Клиент для работы с токенами.
        instruments (InstrumentClient): Клиент для работы с инструментами.
        quotas (QuotasClient): Клиент для работы с квотами.
    """

    def __init__(self, token_manger: TokenManager, auto_refresh_tokens: bool = True):
        """
        Инициализирует главный клиент и все его подклиенты.

        При auto_refresh_tokens=True автоматически настраивает token_client для всех
        подклиентов, чтобы они могли автоматически обновлять JWT токен.

        При auto_refresh_tokens=False необходимо самостоятельно вызвать
        client.access_tokens.set_jwt_token() после создания клиента.

        Параметры:
            token_manger (TokenManager): Менеджер токенов для авторизации.
            auto_refresh_tokens (bool): Включить автоматическое обновление JWT токена.
                По умолчанию True.
        """
        self.account = AccountClient(token_manger)
        self.assets = AssetsClient(token_manger)
        self.orders = OrderClient(token_manger)
        self.access_tokens = TokenClient(token_manger)
        self.instruments = InstrumentClient(token_manger)
        self.quotas = QuotasClient(token_manger)

        if auto_refresh_tokens:
            self.account.set_token_client(self.access_tokens)
            self.assets.set_token_client(self.access_tokens)
            self.orders.set_token_client(self.access_tokens)
            self.instruments.set_token_client(self.access_tokens)
            self.quotas.set_token_client(self.access_tokens)
