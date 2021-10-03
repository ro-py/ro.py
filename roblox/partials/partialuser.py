from ..bases.baseuser import BaseUser
from ..utilities.shared import ClientSharedObject


class PartialUser(BaseUser):
    """
    Attributes:
        _data: The data we get back from the endpoint.
        _shared: The shared object, which is passed to all objects this client generates.
        id: Id of the user
        name: Name of the user
        display_name: display name of the user
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The ClientSharedObject.
            data: The data form the endpoint.
        """
        self._shared: ClientSharedObject = shared
        self._data: dict = data

        self.id: int = data.get("id") or data.get("userId") or data.get("Id")

        super().__init__(shared=shared, user_id=self.id)

        self.name: str = data.get("name") or data.get("Name") or data.get("username") or data.get("Username")
        self.display_name: str = data.get("displayName")


class RequestedUsernamePartialUser(PartialUser):
    """
    Attributes:
        requested_username: Username they requested
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The ClientSharedObject.
            data: The data form the endpoint.
        """
        super().__init__(shared=shared, data=data)

        self.requested_username = data.get("requestedUsername")
