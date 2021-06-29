import roblox.user
import roblox.utilities.clientshardobject
import roblox.utilities.subdomain
import iso8601
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import roblox.bases.basegroup

class JoinRequest:

    def __init__(self, cso: roblox.utilities.clientshardobject.ClientSharedObject,
                 raw_data: dict, group: roblox.bases.basegroup.BaseGroup, user: roblox.user.PartialUser):
        self.cso = cso
        self.group = group
        self.user: roblox.user.PartialUser = user
        self.created = iso8601.parse_date(raw_data['created'])
        self.subdomain: roblox.utilities.subdomain.Subdomain = roblox.utilities.subdomain.Subdomain('groups')

    async def accept(self) -> None:
        """
        Accepts user in to group
        """
        url: str = self.subdomain.generate_endpoint("v1", "groups", self.group.id, "join-requests","users",self.user.id)
        await self.cso.requests.post(url)

    async def decline(self) -> None:
        """
        Declines users join request
        """
        url: str = self.subdomain.generate_endpoint("v1", "groups", self.group.id, "join-requests", "users", self.user.id)
        await self.cso.requests.delete(url)
