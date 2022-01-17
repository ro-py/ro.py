"""

This file contains partial objects related to Roblox groups.

"""
from __future__ import annotations
from typing import TYPE_CHECKING

from ..bases.basegroup import BaseGroup
from ..bases.baseuser import BaseUser

if TYPE_CHECKING:
    from ..client import Client


class AssetPartialGroup(BaseGroup):
    """
    Represents a partial group in the context of a Roblox asset.
    Intended to parse the `data[0]["creator"]` data from https://games.roblox.com/v1/games.

    Attributes:
        _client: The Client object, which is passed to all objects this Client generates.
        id: The group's name.
        creator: The group's owner.
        name: The group's name.
    """

    def __init__(self, client: Client, data: dict):
        """
        Arguments:
            client: The Client.
            data: The data from the endpoint.
        """
        self._client: Client = client

        self.creator: BaseUser = BaseUser(client=client, user_id=data["Id"])
        self.id: int = data["CreatorTargetId"]
        self.name: str = data["Name"]

        super().__init__(client, self.id)

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r}>"


class UniversePartialGroup(BaseGroup):
    """
    Represents a partial group in the context of a Roblox universe.

    Attributes:
        _data: The data we get back from the endpoint.
        _client: The client object, which is passed to all objects this client generates.
        id: Id of the group
        name: Name of the group
    """

    def __init__(self, client: Client, data: dict):
        """
        Arguments:
            client: The ClientSharedObject.
            data: The data from the endpoint.
        """
        self._client: Client = client
        self.id = data["id"]
        self.name: str = data["name"]

        super().__init__(client, self.id)

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r}>"
