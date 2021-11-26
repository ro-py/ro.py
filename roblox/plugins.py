"""

This module contains classes intended to parse and deal with data from Roblox plugin information endpoints.

"""

from datetime import datetime

from dateutil.parser import parse

from .bases.baseplugin import BasePlugin
from .utilities.shared import ClientSharedObject


class Plugin(BasePlugin):
    """
    Represents a Roblox plugin.
    It is intended to parse data from https://develop.roblox.com/v1/plugins.

    Attributes:
        id: The ID of the plugin.
        name: The name of the plugin.
        description: The plugin's description.
        comments_enabled: Whether comments are enabled or disabled.
        version_id: The plugin's current version ID.
        created: When the plugin was created.
        updated: When the plugin was updated.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Attributes:
            shared: The shared object, which is passed to all objects this client generates.
            data: data to make the magic happen.
        """
        super().__init__(shared=shared, plugin_id=data["id"])

        self.id: int = data["id"]
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.comments_enabled: bool = data["commentsEnabled"]
        self.version_id: int = data["versionId"]
        self.created: datetime = parse(data["created"])
        self.updated: datetime = parse(data["updated"])

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r}>"
