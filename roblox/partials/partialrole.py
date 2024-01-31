"""

This file contains partial objects related to Roblox group roles.

"""
from __future__ import annotations
from typing import TYPE_CHECKING

from ..bases.baserole import BaseRole

if TYPE_CHECKING:
    from ..client import Client


class PartialRole(BaseRole):
    """
    Represents partial group role information.

    Attributes:
        _client: The Client object.
        id: The role's ID.
        name: The role's name.
        rank: The role's rank ID.
    """

    def __init__(self, client: Client, data: dict):
        self._client: Client = client

        self.id: int = data["id"]
        super().__init__(client=self._client, role_id=self.id)
        self.name: str = data["name"]
        self.rank: int = data["rank"]
