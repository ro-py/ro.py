import iso8601
from ro_py.bases.baseuser import PartialUser


class Friend(PartialUser):
    def __init__(self, cso, data):
        super().__init__(cso, data)
        self.is_online = data.get('isOnline')
        self.is_deleted = data.get('isDeleted')
        self.description = data["description"]
        self.created = iso8601.parse_date(data["created"])
        self.is_banned = data["isBanned"]
        self.display_name = data["displayName"]


class FriendRequest(Friend):
    def __init__(self, cso, data):
        super(FriendRequest, self).__init__(cso, data)

    async def accept(self):
        accept_req = await self.cso.post(
            url=f"https://friends.roblox.com/v1/users/{self.id}/accept-friend-request"
        )
        return accept_req.status == 200

    async def decline(self):
        accept_req = await self.cso.post(
            url=f"https://friends.roblox.com/v1/users/{self.id}/decline-friend-request"
        )
        return accept_req.status == 200