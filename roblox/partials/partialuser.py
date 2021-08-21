from ..utilities.shared import ClientSharedObject
from ..bases.baseuser import BaseUser


class PartialUser(BaseUser):
    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared
        self._data: dict = data

        self.id: int = data.get("id") or data.get("userId") or data.get("Id")

        super().__init__(shared=shared, user_id=self.id)

        self.name: str = data.get("name") or data.get("username") or data.get("Username")
        self.display_name: str = data.get("displayName")


class RequestedUsernamePartialUser(PartialUser):
    def __init__(self, shared: ClientSharedObject, data: dict):
        super().__init__(shared=shared, data=data)

        self.requested_username = data.get("requestedUsername")
