from finam.base_client.base import BaseClient


class EventClient(BaseClient):
    def __init__(self, token: str):
        super().__init__(token)
        self._url = "/api/v1/events"

    async def get_event(self):
        raise NotImplementedError
