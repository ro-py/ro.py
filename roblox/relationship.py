from .utilities.shared import ClientSharedObject
from enum import Enum

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .bases.basegroup import BaseGroup
    from .groups import Group


class RelationshipType(Enum):
    allys = "Allies"
    enemies = "Enemies"


class RelationshipRequest:
    def __init__(self, shared: ClientSharedObject, data: dict,
                 group: BaseGroup, relationship_type: RelationshipType):
        from .groups import Group
        self.relationship_type: str = relationship_type.value
        self._shared = shared
        self._requests = shared.requests
        self.group = group
        self.requester = Group(shared, data)

    async def accept(self) -> None:
        await self._requests.post(
            self._shared.url_generator.get_url("groups",
                                               f"v1/groups/{self.group.id}/relationships/{self.relationship_type}/requests/{self.requester.id}")
        )

    async def decline(self) -> None:
        await self._requests.delete(
            self._shared.url_generator.get_url("groups",
                                               f"v1/groups/{self.group.id}/relationships/{self.relationship_type}/requests/{self.requester.id}")
        )
