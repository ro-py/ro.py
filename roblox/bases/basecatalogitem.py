"""

This file contains the BaseCatalogItem object, which represents a Roblox catalog item ID.

"""

from __future__ import annotations
from typing import TYPE_CHECKING

from .baseitem import BaseItem

if TYPE_CHECKING:
    from ..client import Client


class BaseCatalogItem(BaseItem):
    """
    Represents a Roblox instance ID.
    Instance IDs represent the ownership of a single Roblox item.

    Attributes:
        id: The item ID.
        item_type: The item's type, either 1 or 2.
    """

    def __init__(self, client: Client, catalog_item_id: int):
        """
        Arguments:
            client: The Client this object belongs to.
            catalog_item_id: The ID of the catalog item.
        """

        self._client: Client = client
        self.id: int = catalog_item_id
        self.item_type: int = catalog_item_type

    # We need to redefine these special methods, as an asset and a bundle can have the same ID but not the same item_type
    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} item_type={self.item_type}>"

    def __eq__(self, other):
        return isinstance(other, self.__class__) and (other.id == self.id) and (other.item_type == self.item_type)

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return (other.id != self.id) and (other.item_type != self.item_type)
        return True
