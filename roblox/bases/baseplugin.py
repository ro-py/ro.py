from ..utilities.shared import ClientSharedObject

from .baseasset import BaseAsset


class BasePlugin(BaseAsset):
    """
    Represents a plugin's ID, with no extra data.
    Plugins are a form of Asset and as such this object derives from BaseAsset.
    """
    def __init__(self, shared: ClientSharedObject, plugin_id: int):
        super().__init__(shared, plugin_id)

        self._shared: ClientSharedObject = shared
        self.id: int = plugin_id

    async def update(self, name: str = None, description: str = None, comments_enabled: str = None):
        """
        Updates the plugin's data.
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
