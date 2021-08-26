from datetime import datetime
from dateutil.parser import parse

from .utilities.shared import ClientSharedObject

from .bases.baseplugin import BasePlugin


class Plugin(BasePlugin):
    """
    Represents a Roblox plugin.
    It is intended to parse data from https://develop.roblox.com/v1/plugins.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        super().__init__(shared=shared, plugin_id=data["id"])

        self.id: int = data["id"]
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.comments_enabled: bool = data["commentsEnabled"]
        self.version_id: int = data["versionId"]
        self.created: datetime = parse(data["created"])
        self.updated: datetime = parse(data["updated"])
