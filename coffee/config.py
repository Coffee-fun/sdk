from os import getenv
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .api_client import CoffeeClient


class _Config:
    api_key: str = getenv("COFFEE_API_KEY")
    _client: "CoffeeClient" = None

    @property
    def api_client(self) -> "CoffeeClient":
        from .api_client import CoffeeClient

        if not self._client:
            self._client = CoffeeClient()
        return self._client

    @api_client.setter
    def api_client(self, cl: "CoffeeClient"):
        self._client = cl


config = _Config()
