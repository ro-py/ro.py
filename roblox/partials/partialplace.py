from roblox import BasePlace
from roblox.utilities.shared import ClientSharedObject


class PartialPlace(BasePlace):
    """
    Attributes:
        id: Id of the Asset
        name: Name of the Asset
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on assets.
            data: The data from the request.
        """
        self.id: int = data.get("TargetId") or data.get("PlaceId")
        super().__init__(shared=shared, place_id=self.id)

        self.name: str = data.get("TargetName") or data.get("PlaceName")

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r}>"


class ActionsPartialPlace(PartialPlace):
    """
    Attributes:
        id: Id of the Asset
        name: Name of the Asset
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on assets.
            data: The data from the request.
        """
        super().__init__(shared=shared, data=data)

        self.type = data["Type"]
        self.actions = data["Actions"]
