"""

This file contains the BasePlugin object, which represents a Roblox plugin ID.

"""

from .baseasset import BaseAsset
from ..utilities.shared import ClientSharedObject


class BasePlugin(BaseAsset):
    """
    Represents a Roblox plugin ID.
    Plugins are a form of Asset and as such this object derives from BaseAsset.

    Attributes:
        _shared: The ClientSharedObject.
        id: The plugin ID.
    """

    def __init__(self, shared: ClientSharedObject, plugin_id: int):
        """
        Arguments:
            shared: The ClientSharedObject.
            plugin_id: The plugin ID.
        """

        super().__init__(shared, plugin_id)

        self._shared: ClientSharedObject = shared
        self.id: int = plugin_id

    async def update(self, name: str = None, description: str = None, comments_enabled: str = None):
        """
        Updates the plugin's data.

        Arguments:
            name: The new group name.
            description: The new group description.
            comments_enabled: Whether to enable comments.
        """
        await self._shared.requests.patch(
            url=self._shared.url_generator.get_url(
                "develop", f"v1/plugins/{self.id}"
            ),
            json={
                "name": name,
                "description": description,
                "commentsEnabled": comments_enabled
            }
        )
