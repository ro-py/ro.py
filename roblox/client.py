from typing import Union

from .utilities.shared import ClientSharedObject
from .utilities.url import URLGenerator
from .utilities.requests import Requests
from .utilities.iterators import PageIterator

from .users import User
from .groups import Group

from .bases.baseuser import BaseUser
from .bases.basegroup import BaseGroup

from .partials.partialuser import PartialUser, RequestedUsernamePartialUser


class Client:
    def __init__(self, token: str = None, base_url: str = "roblox.com"):
        self._requests: Requests = Requests()
        """
        The requests object, which is used to send requests to Roblox endpoints.
        !!! note
            It is not recommended to initialize this object alone without a Client.
            Ideally, you should always generate a client, even when sending requests, as it allows you to use our
            builtin authentication methods and still recieve fixes in case of API changes that break existing code.
            
        """

        self._url_generator: URLGenerator = URLGenerator(base_url=base_url)
        """
        The URL generator object, which is used to generate URLs to send requests to endpoints.
        """

        self._shared: ClientSharedObject = ClientSharedObject(
            client=self,
            requests=self._requests,
            url_generator=self._url_generator
        )
        """
        The shared object, which is shared between all objects the client generates.
        """

        if token:
            self.set_token(token)

    def set_token(self, token: str):
        """
        Sets the .ROBLOSECURITY token.
        """
        self._requests.session.cookies[".ROBLOSECURITY"] = token

    async def get_user(self, user_id: int) -> User:
        """
        Returns a user with the specified user ID.
        """
        user_response = await self._requests.get(
            url=self._shared.url_generator.get_url("users", f"v1/users/{user_id}")
        )
        user_data = user_response.json()
        return User(
            shared=self._shared,
            data=user_data
        )

    async def get_authenticated_user(self, expand: bool = True) -> Union[User, PartialUser]:
        """
        Returns the authenticated user.
        If the "expand" property is True, returns a User. If not, it returns a PartialUser.
        """
        authenticated_user_response = await self._requests.get(
            url=self._shared.url_generator.get_url("users", f"v1/users/authenticated")
        )
        authenticated_user_data = authenticated_user_response.json()

        if expand:
            return await self.get_user(authenticated_user_data["id"])
        else:
            return PartialUser(
                shared=self._shared,
                data=authenticated_user_data
            )

    async def get_users(
            self,
            user_ids: list[int],
            exclude_banned_users: bool = False,
            expand: bool = False
    ) -> Union[list[PartialUser], list[User]]:
        """
        Returns a list of users corresponding to each user ID in the list.
        If the "expand" property is True, returns a list of User. If not, returns a list of PartialUser.
        """
        users_response = await self._requests.post(
            url=self._shared.url_generator.get_url("users", f"v1/users"),
            json={
                "userIds": user_ids,
                "excludeBannedUsers": exclude_banned_users
            }
        )
        users_data = users_response.json()["data"]

        if expand:
            return [await self.get_user(user_data["id"]) for user_data in users_data]
        else:
            return [PartialUser(
                shared=self._shared,
                data=user_data
            ) for user_data in users_data]

    async def get_users_by_usernames(
            self,
            usernames: list[str],
            exclude_banned_users: bool = False,
            expand: bool = False
    ) -> Union[list[RequestedUsernamePartialUser], list[User]]:
        """
        Returns a list of users corresponding to each user ID in the list.
        If the "expand" property is True, returns a list of User. If not, returns a list of PartialUser.
        """
        users_response = await self._requests.post(
            url=self._shared.url_generator.get_url("users", f"v1/usernames/users"),
            json={
                "usernames": usernames,
                "excludeBannedUsers": exclude_banned_users
            }
        )
        users_data = users_response.json()["data"]

        if expand:
            return [await self.get_user(user_data["id"]) for user_data in users_data]
        else:
            return [RequestedUsernamePartialUser(
                shared=self._shared,
                data=user_data
            ) for user_data in users_data]

    async def get_user_by_username(
            self,
            username: str,
            exclude_banned_users: bool = False,
            expand: bool = False
    ):
        users = await self.get_users_by_usernames(
            usernames=[username],
            exclude_banned_users=exclude_banned_users,
            expand=expand
        )
        try:
            return users[0]
        except IndexError:
            return None

    def get_base_user(self, user_id: int) -> BaseUser:
        return BaseUser(shared=self._shared, user_id=user_id)

    def _user_search_handler(self, data: dict) -> RequestedUsernamePartialUser:
        return RequestedUsernamePartialUser(shared=self._shared, data=data)

    def user_search(self, keyword: str, limit: int = 10) -> PageIterator:
        return PageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url("users", f"v1/users/search"),
            limit=limit,
            extra_parameters={
                "keyword": keyword
            },
            item_handler=self._user_search_handler
        )

    async def get_group(self, group_id: int) -> Group:
        group_response = await self._requests.get(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{group_id}")
        )
        group_data = group_response.json()
        return Group(
            shared=self._shared,
            data=group_data
        )

    def get_base_group(self, group_id: int) -> BaseGroup:
        return BaseGroup(shared=self._shared, group_id=group_id)
