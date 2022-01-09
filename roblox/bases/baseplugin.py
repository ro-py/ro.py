"""

This file contains the BasePlugin object, which represents a Roblox plugin ID.

"""

from __future__ import annotations
from typing import TYPE_CHECKING

from .baseasset import BaseAsset

if TYPE_CHECKING:
    from ..client import Client


class BasePlugin(BaseAsset):
    """
    Represents a Roblox plugin ID.
    Plugins are a form of Asset and as such this object derives from BaseAsset.

    Attributes:
        id: The plugin ID.
    """

    def __init__(self, client: Client, plugin_id: int):
        """
        Arguments:
            client: The Client this object belongs to.
            plugin_id: The plugin ID.
        """

        super().__init__(client, plugin_id)

        self._client: Client = client
        self.id: int = plugin_id

    async def update(self, name: str = None, description: str = None, comments_enabled: str = None):
        """
        Updates the plugin's data.

        Arguments:
            name: The new group name.
            description: The new group description.
            comments_enabled: Whether to enable comments.
        """
        await self._client.requests.patch(
            url=self._client.url_generator.get_url(
                "develop", f"v1/plugins/{self.id}"
            ),
            json={
                "name": name,
                "description": description,
                "commentsEnabled": comments_enabled
            }
        )
