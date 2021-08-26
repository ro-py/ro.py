from typing import Union, Optional

from .utilities.shared import ClientSharedObject
from .utilities.url import URLGenerator
from .utilities.requests import Requests
from .utilities.iterators import PageIterator

from .users import User
from .groups import Group
from .universes import Universe
from .places import Place
from .assets import EconomyAsset
from .plugins import Plugin

from .presence import PresenceProvider
from .thumbnails import ThumbnailProvider
from .delivery import DeliveryProvider

from .bases.baseuser import BaseUser
from .bases.basegroup import BaseGroup
from .bases.baseuniverse import BaseUniverse
from .bases.baseplace import BasePlace
from .bases.baseasset import BaseAsset
from .bases.baseplugin import BasePlugin

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
            client=self, requests=self._requests, url_generator=self._url_generator
        )
        """
        The shared object, which is shared between all objects the client generates.
        """

        self.presence: PresenceProvider = PresenceProvider(shared=self._shared)
        """
        The presence provider object.
        """
        self.thumbnails: ThumbnailProvider = ThumbnailProvider(shared=self._shared)
        """
        The thumbnail provider object.
        """
        self.delivery: DeliveryProvider = DeliveryProvider(shared=self._shared)
        """
        The delivery provider object.
        """

        self._shared.presence_provider = self.presence  # TODO: Improve this hack
        self._shared.thumbnail_provider = self.thumbnails
        self._shared.delivery_provider = self.delivery

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
        return User(shared=self._shared, data=user_data)

    async def get_authenticated_user(
        self, expand: bool = True
    ) -> Union[User, PartialUser]:
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
            return PartialUser(shared=self._shared, data=authenticated_user_data)

    async def get_users(
        self,
        user_ids: list[int],
        exclude_banned_users: bool = False,
        expand: bool = False,
    ) -> Union[list[PartialUser], list[User]]:
        """
        Returns a list of users corresponding to each user ID in the list.
        If the "expand" property is True, returns a list of User. If not, returns a list of PartialUser.
        """
        users_response = await self._requests.post(
            url=self._shared.url_generator.get_url("users", f"v1/users"),
            json={"userIds": user_ids, "excludeBannedUsers": exclude_banned_users},
        )
        users_data = users_response.json()["data"]

        if expand:
            return [await self.get_user(user_data["id"]) for user_data in users_data]
        else:
            return [
                PartialUser(shared=self._shared, data=user_data)
                for user_data in users_data
            ]

    async def get_users_by_usernames(
        self,
        usernames: list[str],
        exclude_banned_users: bool = False,
        expand: bool = False,
    ) -> Union[list[RequestedUsernamePartialUser], list[User]]:
        """
        Returns a list of users corresponding to each username in the list.
        If the "expand" property is True, returns a list of User. If not, returns a list of PartialUser.
        """
        users_response = await self._requests.post(
            url=self._shared.url_generator.get_url("users", f"v1/usernames/users"),
            json={"usernames": usernames, "excludeBannedUsers": exclude_banned_users},
        )
        users_data = users_response.json()["data"]

        if expand:
            return [await self.get_user(user_data["id"]) for user_data in users_data]
        else:
            return [
                RequestedUsernamePartialUser(shared=self._shared, data=user_data)
                for user_data in users_data
            ]

    async def get_user_by_username(
        self, username: str, exclude_banned_users: bool = False, expand: bool = False
    ) -> Optional[Union[list[RequestedUsernamePartialUser], list[User]]]:
        """
        Returns a user corresponding to the passed username.
        If the "expand" property is True, returns a User. If not, returns a PartialUser.
        """
        users = await self.get_users_by_usernames(
            usernames=[username],
            exclude_banned_users=exclude_banned_users,
            expand=expand,
        )
        try:
            return users[0]
        except IndexError:
            return None

    def get_base_user(self, user_id: int) -> BaseUser:
        """
        Gets a base user.
        This method does not send any requests - it just generates a BaseUser object.
        Passing an invalid user ID to this method will not raise an error until you use one of the BaseUser methods.
        Use this method when you want to use one of the BaseUser methods without grabbing information about the user.
        """
        return BaseUser(shared=self._shared, user_id=user_id)

    def _user_search_handler(self, shared: ClientSharedObject, data: dict) -> RequestedUsernamePartialUser:
        return RequestedUsernamePartialUser(shared=shared, data=data)

    def user_search(self, keyword: str, limit: int = 10) -> PageIterator:
        """
        Search for users with a keyword.
        """
        return PageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url("users", f"v1/users/search"),
            limit=limit,
            extra_parameters={"keyword": keyword},
            item_handler=self._user_search_handler,
        )

    async def get_group(self, group_id: int) -> Group:
        """
        Gets a group by its ID.
        """
        group_response = await self._requests.get(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{group_id}")
        )
        group_data = group_response.json()
        return Group(shared=self._shared, data=group_data)

    def get_base_group(self, group_id: int) -> BaseGroup:
        """
        Gets a base group.
        This method does not send any requests - it just generates a BaseGroup object.
        Passing an invalid group ID to this method will not raise an error until you use one of the BaseGroup methods.
        Use this method when you want to use one of the BaseGroup methods without grabbing information about the group.
        """
        return BaseGroup(shared=self._shared, group_id=group_id)

    async def get_universes(self, universe_ids: list[int]) -> list[Universe]:
        """
        Returns a list of universes corresponding to each ID in the list.
        """
        universes_response = await self._requests.get(
            url=self._shared.url_generator.get_url("games", f"v1/games"),
            params={"universeIds": universe_ids},
        )
        universes_data = universes_response.json()["data"]
        return [
            Universe(shared=self._shared, data=universe_data)
            for universe_data in universes_data
        ]

    async def get_universe(self, universe_id: int) -> Optional[Universe]:
        """
        Gets a universe with the passed ID.
        """
        universes = await self.get_universes(universe_ids=[universe_id])
        try:
            return universes[0]
        except IndexError:
            return None

    def get_base_universe(self, universe_id: int) -> BaseUniverse:
        """
        Gets a base universe.
        """
        return BaseUniverse(shared=self._shared, universe_id=universe_id)

    async def get_places(self, place_ids: list[int]) -> list[Place]:
        """
        Returns a list of places corresponding to each ID in the list.
        """
        places_response = await self._requests.get(
            url=self._shared.url_generator.get_url(
                "games", f"v1/games/multiget-place-details"
            ),
            params={"placeIds": place_ids},
        )
        places_data = places_response.json()
        return [
            Place(shared=self._shared, data=place_data) for place_data in places_data
        ]

    async def get_place(self, place_id: int) -> Optional[Place]:
        """
        Gets a place with the passed ID.
        """
        places = await self.get_places(place_ids=[place_id])
        try:
            return places[0]
        except IndexError:
            return None

    def get_base_place(self, place_id: int) -> BasePlace:
        """
        Gets a base place.
        """
        return BasePlace(shared=self._shared, place_id=place_id)

    async def get_asset(self, asset_id: int) -> EconomyAsset:
        """
        Gets an asset with the passed ID.
        """
        asset_response = await self._requests.get(
            url=self._shared.url_generator.get_url(
                "economy", f"v2/assets/{asset_id}/details"
            )
        )
        asset_data = asset_response.json()
        return EconomyAsset(shared=self._shared, data=asset_data)

    def get_base_asset(self, asset_id: int) -> BaseAsset:
        """
        Gets a base asset.
        """
        return BaseAsset(shared=self._shared, asset_id=asset_id)

    async def get_plugins(self, plugin_ids: list[int]) -> list[Plugin]:
        plugins_response = await self._requests.get(
            url=self._shared.url_generator.get_url(
                "develop", "v1/plugins"
            ),
            params={
                "pluginIds": plugin_ids
            }
        )
        plugins_data = plugins_response.json()["data"]
        return [Plugin(shared=self._shared, data=plugin_data) for plugin_data in plugins_data]

    async def get_plugin(self, plugin_id: int) -> Optional[Plugin]:
        plugins = await self.get_plugins([plugin_id])
        try:
            return plugins[0]
        except IndexError:
            return None

    def get_base_plugin(self, plugin_id: int) -> BasePlugin:
        """
        Gets a base plugin.
        """
        return BasePlugin(shared=self._shared, plugin_id=plugin_id)