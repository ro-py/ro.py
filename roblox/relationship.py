from .utilities.shared import ClientSharedObject
from .groups import Group
import roblox.bases.basegroup
from enum import Enum


class RelationshipType(Enum):
    ALLYS = "Allys"
    ENEMIES = "Enemies"


class RelationshipRequest:
    def __init__(self, shared: ClientSharedObject, data: dict,
                 group: roblox.bases.basegroup, relationship_type: RelationshipType):
        self.relationship_type: str = relationship_type.value
        self._shared = shared
        self._requests = shared.requests
        self.group = group
        self.requester = Group(shared, data)

    async def accept(self) -> None:
        await self._requests.post(
            self._shared.url_generator.get_url("groups",f"v1/groups/{self.group.id}/relationships/{self.relationship_type}/requests/{self.requester.id}")
        )

    async def decline(self) -> None:
        await self._requests.delete(
            self._shared.url_generator.get_url("groups",f"v1/groups/{self.group.id}/relationships/{self.relationship_type}/requests/{self.requester.id}")
        )
