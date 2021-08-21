from datetime import datetime
from dateutil.parser import parse


class User:
    def __init__(self, data: dict):
        self._data: dict = data

        self.name: str = data["name"]
        self.display_name: str = data["displayName"]
        self.external_app_display_name: str = data["externalAppDisplayName"]
        self.id: int = data["id"]
        self.is_banned: bool = data["isBanned"]
        self.description: str = data["description"]
        self.created: datetime = parse(data["created"])
