from datetime import datetime
from dateutil.parser import parse

from .utilities.shared import ClientSharedObject

from .bases.baseuser import BaseUser


class User(BaseUser):
    def __init__(self, shared: ClientSharedObject, data: dict):
        super().__init__(shared=shared, user_id=data["id"])

        self._shared = shared
        self._data: dict = data

        self.name: str = data["name"]
        self.display_name: str = data["displayName"]
        self.external_app_display_name: str = data["externalAppDisplayName"]
        self.id: int = data["id"]
        self.is_banned: bool = data["isBanned"]
        self.description: str = data["description"]
        self.created: datetime = parse(data["created"])
