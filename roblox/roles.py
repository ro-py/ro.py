from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .bases.basegroup import BaseGroup
    from .utilities.shared import ClientSharedObject


class Role:
    """
    Represents a role of a group.
    """

    def __init__(self, shared: ClientSharedObject, group: BaseGroup, data: dict):
        """
        Arguments:
            shared: Shared object.
            group: The group the role belongs to.
            data: The data from the request to get the role.
        """
        self._shared = shared
        self._requests = shared.requests
        self._data = data

        self.group = group
        """The group the role belongs to."""
        self.id: int = data['id']
        """The id of the role."""
        self.name: str = data['name']
        """The name of the role."""
        self.description: str = data['description']
        """The description of the role."""
        self.rank: int = data['rank']
        """The rank number of the role. (1-255)"""
        self.member_count = data['memberCount']
        """How many members have the role in the group."""

    async def edit(self, name: str = None, rank: int = None, description: str = None):
        """
        Arguments:
            name: The new name of the role.
            rank: The new rank number of the role.
            description: The new description of the role.
        """
        self._data['name'] = name
        self._data['rank'] = rank
        self._data['description'] = description

        await self._requests.patch(
            url=self._shared.url_generator.get_url("group", f"v1/groups/{self.group.id}/rolesets/{self.id}"),
            json=self._data
        )