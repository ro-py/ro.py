from .utilities.shared import ClientSharedObject

from .partials.partialuser import PartialUser

from .bases.basegroup import BaseGroup


class Group(BaseGroup):
    def __init__(self, shared: ClientSharedObject, data: dict):
        super().__init__(shared, data["id"])

        self._shared: ClientSharedObject = shared
        self._data: dict = data

        self.id: int = data["id"]
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.owner: PartialUser = PartialUser(shared=shared, data=data["owner"])
        self.shout: str = data["shout"]
        self.member_count: int = data["memberCount"]
        self.is_builders_club_only: bool = data["isBuildersClubOnly"]
        self.public_entry_allowed: bool = data["publicEntryAllowed"]
