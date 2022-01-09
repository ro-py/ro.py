"""

This file contains the BaseUniverseSocialLink object, which represents a Roblox social link ID.

"""

from __future__ import annotations
from typing import TYPE_CHECKING

from .baseitem import BaseItem

if TYPE_CHECKING:
    from ..client import Client


class BaseUniverseSocialLink(BaseItem):
    """
    Represents a Roblox universe social link ID.

    Attributes:
        id: The universe social link ID.
    """

    def __init__(self, client: Client, social_link_id: int):
        """
        Arguments:
            client: The Client this object belongs to.
            social_link_id: The universe social link ID.
        """

        self._client: Client = client
        self.id: int = social_link_id
