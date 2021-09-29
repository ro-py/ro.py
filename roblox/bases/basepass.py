from ..utilities.shared import ClientSharedObject


class BasePass:
    """
    Represents a Roblox gamepass ID.

    Attributes:
        _shared: The ClientSharedObject.
        id: The gamepass ID.
    """

    def __init__(self, shared: ClientSharedObject, pass_id: int):
        """
        Arguments:
            shared: The ClientSharedObject.
            pass_id: The gamepass ID.
        """

        self._shared: ClientSharedObject = shared
        self.id: int = pass_id
