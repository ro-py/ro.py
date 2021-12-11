from roblox import BaseGamePass
from roblox.utilities.shared import ClientSharedObject


class PartialGamePass(BaseGamePass):
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
        self.id: int = data["GamePassId"]
        super().__init__(shared=shared, gamepass_id=self.id)

        self.name: str = data["GamePassName"]

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r}>"
