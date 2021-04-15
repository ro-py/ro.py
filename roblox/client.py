from roblox.utilities.requests import Requests
from roblox.utilities.subdomain import Subdomain


class ClientSharedObject:
    def __init__(self, cookie):
        self.requests = Requests()


class Client:
    def __init__(self, cookie):
        self.cso = ClientSharedObject(cookie)

    async def get_group(self, group_id):
        subdomain = Subdomain('group')
        url = subdomain.generate_endpoint("v1", "groups", group_id)
        response = await self.cso.requests.get(url)

    async def get_user(self, user_id):
        pass
