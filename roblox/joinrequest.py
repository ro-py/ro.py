from __future__ import annotations
from roblox.utilities.clientsharedobject import ClientSharedObject
from roblox.bases.basegroup import BaseGroup
from roblox.user import PartialUser
import roblox.bases.basegroup
import roblox.utilities.subdomain
import iso8601
import roblox.bases.basegroup


class JoinRequest:

    def __init__(self: JoinRequest, cso: ClientSharedObject, raw_data: dict, group: BaseGroup, user: PartialUser):
        self.cso = cso
        self.group = group
        self.user = user
        self.created = iso8601.parse_date(raw_data['created'])
        self.subdomain = roblox.utilities.subdomain.Subdomain('groups')

    async def accept(self: JoinRequest) -> None:
        """
        Accepts user in to group
        """
        url = self.subdomain.generate_endpoint("v1", "groups", self.group.id, "join-requests", "users", self.user.id)
        await self.cso.requests.post(url)

    async def decline(self: JoinRequest) -> None:
        """
        Denies users join request
        """

        url = self.subdomain.generate_endpoint("v1", "groups", self.group.id, "join-requests", "users", self.user.id)
        await self.cso.requests.delete(url)