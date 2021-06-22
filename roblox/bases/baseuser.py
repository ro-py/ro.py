from httpx import Response

from roblox.utilities.requests import Requests
from roblox.utilities.subdomain import Subdomain


class BaseUser:
    """
    Represents a user with as little information possible.
    """
    def __init__(self, cso, user_id):
        self.cso = cso
        """A client shared object."""
        self.requests: Requests = cso.requests
        """A requests object."""
        self.id: int = user_id
        """The id of the user."""
        self.subdomain: Subdomain = Subdomain('users')
        """Subdomain users.roblox.com"""

    async def add_friend(self) -> int:
        """
        Sends a friend request to the user.
        """
        url: str = self.subdomain.generate_endpoint("v1", "users", self.id, "request-friendship")
        response: Response = await self.requests.post(url)
        return response.status_code

    async def unfriend(self) -> int:
        """
        Removes the user from the authenticated users friends list.
        """
        url: str = self.subdomain.generate_endpoint("v1", "users", self.id, "unfriend")
        response: Response = await self.requests.post(url)
        return response.status_code

    async def block(self) -> int:
        """
        Blocks the user on the authenticated users account.
        """
        data: dict = {
            "userId": self.id
        }
        response: Response = await self.requests.post("https://www.roblox.com/userblock/blockuser", json=data)
        return response.status_code

    async def unblock(self) -> int:
        """
        Blocks the user on the authenticated users account.
        """
        data: dict = {
            "userId": self.id
        }
        response: Response = await self.requests.post("https://www.roblox.com/userblock/unblock", json=data)
        return response.status_code
