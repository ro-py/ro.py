from __future__ import annotations

import roblox.group
import roblox.utilities.clientsharedobject
import roblox.utilities.subdomain
import roblox.bases.basegroup
from enum import Enum

class RelationshipType(Enum):
    ALLYS = "Allys"
    ENEMIES = "Enemies"


class RelationshipRequest:
    def __init__(self, cso: roblox.utilities.clientsharedobject.ClientSharedObject, raw_data: dict,
                 group: roblox.bases.basegroup, relationship_type: RelationshipType):
        self.relationship_type: str = relationship_type.value
        self.cso = cso
        self.requests = cso.requests
        self.group = group
        self.requester = roblox.group.Group(cso, raw_data)
        self.subdomain: roblox.utilities.subdomain.Subdomain = roblox.utilities.subdomain.Subdomain("groups")

    async def accept(self):
        url: str = self.subdomain.generate_endpoint("v1", "groups", self.group.id, "relationships",
                                                    self.relationship_type, "requests", self.requester.id)
        self.requests.post(url)

    async def decline(self):
        url: str = self.subdomain.generate_endpoint("v1", "groups", self.group.id, "relationships",
                                                    self.relationship_type, "requests", self.requester.id)
        self.requests.delete(url)
