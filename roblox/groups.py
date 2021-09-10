from .shout import Shout
from .utilities.shared import ClientSharedObject

from .partials.partialuser import PartialUser

from .bases.basegroup import BaseGroup


class Group(BaseGroup):
    """
    Represents a Join Request

    Attributes:
        _shared: The shared object, which is passed to all objects this client generates.
        _data: The raw data we got back form the endpoint.
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
        self._data: dict = data

        self.id: int = data["id"]
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.owner: PartialUser = PartialUser(shared=shared, data=data["owner"])
        self.shout: Shout = Shout(shared, self, data["shout"])
        self.member_count: int = data["memberCount"]
        self.is_builders_club_only: bool = data["isBuildersClubOnly"]
        self.public_entry_allowed: bool = data["publicEntryAllowed"]
        self.is_locked: bool = data.get("isLocked") or False
