"""

This file contains the BaseUniverseSocialLink object, which represents a Roblox social link ID.

"""

from .baseitem import BaseItem
from ..utilities.shared import ClientSharedObject


class BaseUniverseSocialLink(BaseItem):
    """
    Represents a Roblox universe social link ID.

    Attributes:
        _shared: The ClientSharedObject.
        id: The universe social link ID.
    """

    def __init__(self, shared: ClientSharedObject, social_link_id: int):
        """
        Arguments:
            shared: The ClientSharedObject.
            social_link_id: The universe social link ID.
        """

        self._shared: ClientSharedObject = shared
        self.id: int = social_link_id
