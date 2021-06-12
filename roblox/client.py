from roblox.user import User
from roblox.group import Group
from roblox.utilities.requests import Requests
from roblox.utilities.subdomain import Subdomain


class ClientSharedObject:
    def __init__(self, cookie):
        self.requests = Requests()


class Client:
    def __init__(self, cookie):
        self.cso: ClientSharedObject = ClientSharedObject(cookie)

    async def get_group(self, group_id: int) -> Group:
        """
        Creates a group object using the provided group id.

        Parameters
        ----------
        group_id : int
            The id of the group.

        Returns
        -------
        roblox.group.Group

        """
        subdomain = Subdomain('group')
        url = subdomain.generate_endpoint("v1", "groups", group_id)
        response = await self.cso.requests.get(url)
        data = response.json()
        return Group(self.cso, data)

    async def get_user(self, user_id: int) -> User:
        """
        Creates a user object using the provided user id.

        Parameters
        ----------
        user_id : int
            The id of the user.

        Returns
        -------
        roblox.user.User
        """
        subdomain = Subdomain('users')
        url = subdomain.generate_endpoint("v1", "users", user_id)
        response = await self.cso.requests.get(url)
        data = response.json()
        return User(self.cso, data)

    async def get_user_by_id(self, user_id: int) -> User:
        """
        Alias of get_user

        Parameters
        ----------
        user_id : int
            The id of the user.

        Returns
        -------
        roblox.user.User
        """
        return await self.get_user(user_id)

    async def get_user_by_username(self, name: str) -> User:
        """
        Gets a user using a username.

        Parameters
        ----------
        name : str
                The name of the user

        Returns
        -------
        roblox.user.User
        """
        params = {
            "username": name
        }
        request = await self.cso.requests.get(f'https://api.roblox.com/users/get-by-username', params=params)
        response = request.json()
        return await self.get_user(response.get("Id"))
 