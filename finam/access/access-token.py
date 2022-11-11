from finam.base_client.base import BaseClient


class TokenClient(BaseClient):
    def __init__(self, token: str):
        super().__init__(token)
        self._url = "/api/v1/my/access-tokens"

    async def get_tokens(self):
        raise NotImplementedError

    async def create_token(self):
        raise NotImplementedError

    async def get_token(self):
        raise NotImplementedError

    async def delete_token(self):
        raise NotImplementedError

    async def check_token(self):
        raise NotImplementedError
