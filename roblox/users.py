from datetime import datetime
from dateutil.parser import parse

from .utilities.shared import ClientSharedObject

from .bases.baseuser import BaseUser


class User(BaseUser):
    """
    Represents a single conversation.

    Attributes:
        _shared: The shared object, which is passed to all objects this client generates.
        id: The id of the current user
        name: The name of the current user
        display_name: The display name of the current user
        external_app_display_name: The external app display name of the current user
        is_banned: If the user is banned
        description: The description the current user wrote for himself
        created: When the user created his account
    """
    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: Shared object.
            data: The data form the request.
        """
        super().__init__(shared=shared, user_id=data["id"])

        self._shared: ClientSharedObject = shared
        self._data: dict = data

        self.name: str = data["name"]
        self.display_name: str = data["displayName"]
        self.external_app_display_name: str = data["externalAppDisplayName"]
        self.id: int = data["id"]
        self.is_banned: bool = data["isBanned"]
        self.description: str = data["description"]
        self.created: datetime = parse(data["created"])
