from typing import Union

from .utilities.shared import ClientSharedObject
from .utilities.url import URLGenerator
from .utilities.requests import Requests

from .users import User

from .partials.partialuser import PartialUser


class Client:
    def __init__(self, cookie: str = None, base_url: str = "roblox.com"):
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

    async def get_authenticated_user(self, expand=True) -> Union[User, PartialUser]:
        """
        Returns the authenticated user.
        If the "expand" property is set to True, returns a User. If not, it returns a PartialUser.
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
