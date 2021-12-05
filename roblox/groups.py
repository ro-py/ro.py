"""

Contains classes related to Roblox group data and parsing.

"""

from typing import Optional, Tuple

from .bases.basegroup import BaseGroup
from .partials.partialuser import PartialUser
from .shout import Shout
from .utilities.shared import ClientSharedObject


class Group(BaseGroup):
    """
    Represents a group.

    Attributes:
        _shared: The shared object, which is passed to all objects this client generates.
        id: the id of the group.
        name: name of the group.
        description: description of the group.
        owner: player who owns the group.
        shout: the current group shout.
        member_count: about of members in the group.
        is_builders_club_only: can only people with builder club join.
        public_entry_allowed: can you join without your join request having to be accepted.
        is_locked: Is the group locked?
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            data: The data we get back from the endpoint.
            shared: The shared object, which is passed to all objects this client generates.
        """
        super().__init__(shared, data["id"])

        self._shared: ClientSharedObject = shared

        self.id: int = data["id"]
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.owner: Optional[PartialUser] = PartialUser(shared=shared, data=data["owner"]) if data.get("owner") else \
            None
        self.shout: Optional[Shout] = Shout(
            shared=self._shared,
            data=data["shout"]
        ) if data.get("shout") else None

        self.member_count: int = data["memberCount"]
        self.is_builders_club_only: bool = data["isBuildersClubOnly"]
        self.public_entry_allowed: bool = data["publicEntryAllowed"]
        self.is_locked: bool = data.get("isLocked") or False

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r} owner={self.owner}>"

    async def update_shout(self, message: str, update_self: bool = True) -> Tuple[Optional[Shout], Optional[Shout]]:
        """
        Updates the shout.

        Arguments:
            message: The new shout message.
            update_self: Whether to update self.shout automatically.
        Returns: 
            The old and new shout.
        """
        shout_response = await self._requests.patch(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.id}/status"),
            json={
                "message": message
            }
        )

        shout_data = shout_response.json()

        old_shout: Optional[Shout] = self.shout
        new_shout: Optional[Shout] = shout_data and Shout(
            shared=self._shared,
            data=shout_data
        ) or None

        if update_self:
            self.shout = new_shout

        return old_shout, new_shout
