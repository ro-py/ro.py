from typing import Union, Optional, List

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
    """
    Represents a Roblox client.

    Attributes:
        _requests: The requests object, which is used to send requests to Roblox endpoints.
        _url_generator: The URL generator object, which is used to generate URLs to send requests to endpoints.
        _shared: The shared object, which is passed to all objects this client generates.
        presence: The presence provider object.
        thumbnails: The thumbnail provider object.
        delivery: The delivery provider object.
    """

    def __init__(self, token: str = None, base_url: str = "roblox.com", parse_bans: bool = True):
        """
        Arguments:
            token: A .ROBLOSECURITY token to authenticate the client with.
            base_url: The base URL to use when sending requests.
        """
        self._url_generator: URLGenerator = URLGenerator(base_url=base_url)
        self._requests: Requests = Requests(
            url_generator=self._url_generator,
            parse_bans=parse_bans
        )
        self._shared: ClientSharedObject = ClientSharedObject(
            client=self,
            requests=self._requests,
            url_generator=self._url_generator
        )

        self.presence: PresenceProvider = PresenceProvider(shared=self._shared)
        self.thumbnails: ThumbnailProvider = ThumbnailProvider(shared=self._shared)
        self.delivery: DeliveryProvider = DeliveryProvider(shared=self._shared)

        # TODO: Improve this hack
        self._shared.presence_provider = self.presence
        self._shared.thumbnail_provider = self.thumbnails
        self._shared.delivery_provider = self.delivery

        if token:
            self.set_token(token)

    def set_token(self, token: str) -> None:
        """
        Authenticates the client with the passed .ROBLOSECURITY token.
        This method does not send any requests and will not throw if the token is invalid.

        Arguments:
            token: A .ROBLOSECURITY token to authenticate the client with.

        """
        self._requests.session.cookies[".ROBLOSECURITY"] = token

    async def get_user(self, user_id: int) -> User:
        """
        Gets a user with the specified user ID.

        Arguments:
            user_id: A Roblox user ID.

        Returns:
            A user object.
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
        Grabs the authenticated user.

        Arguments:
            expand: Whether to return a User (2 requests) rather than a PartialUser (1 request)

        Returns:
            The authenticated user.
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
            user_ids: List[int],
            exclude_banned_users: bool = False,
            expand: bool = False,
    ) -> Union[List[PartialUser], List[User]]:
        """
        Grabs a list of users corresponding to each user ID in the list.

        Arguments:
            user_ids: A list of Roblox user IDs.
            exclude_banned_users: Whether to exclude banned users from the data.
            expand: Whether to return a list of Users (2 requests) rather than PartialUsers (1 request)

        Returns:
            A List of Users or partial users.
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
            usernames: List[str],
            exclude_banned_users: bool = False,
            expand: bool = False,
    ) -> Union[List[RequestedUsernamePartialUser], List[User]]:
        """
        Grabs a list of users corresponding to each username in the list.

        Arguments:
            usernames: A list of Roblox usernames.
            exclude_banned_users: Whether to exclude banned users from the data.
            expand: Whether to return a list of Users (2 requests) rather than RequestedUsernamePartialUsers (1 request)

        Returns:
            A list of User or RequestedUsernamePartialUser, depending on the expand argument.
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
    ) -> Optional[Union[RequestedUsernamePartialUser, User]]:
        """
        Grabs a user corresponding to the passed username.

        Arguments:
            username: A Roblox username.
            exclude_banned_users: Whether to exclude banned users from the data.
            expand: Whether to return a User (2 requests) rather than a RequestedUsernamePartialUser (1 request)

        Returns:
            A User, RequestedUsernamePartialUser, or None, depending on the expand argument.
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
        FIXME
        This method does not send any requests - it just generates a BaseUser object.

        Arguments:
            user_id: A Roblox user ID.

        Returns:
            A BaseUser.
        """
        return BaseUser(shared=self._shared, user_id=user_id)

    def _user_search_handler(self, shared: ClientSharedObject, data: dict) -> RequestedUsernamePartialUser:
        """
        Handler for converting data from users/v1/users/search to a RequestedUsernamePartialUser.

        Arguments:
            shared: A ClientSharedObject to pass to the output object.
            data: One item from users/v1/users/search.

        Returns:
            A RequestedUsernamePartialUser.
        """
        return RequestedUsernamePartialUser(shared=shared, data=data)

    def user_search(self, keyword: str, limit: int = 10) -> PageIterator:
        """
        Search for users with a keyword.

        Arguments:
            keyword: A keyword to search for.
            limit: How many users should be returned for each page

        Returns:
            A PageIterator containing RequestedUsernamePartialUser.
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

        Arguments:
            group_id: A Roblox group ID.

        Returns:
            A Group.
        """
        group_response = await self._requests.get(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{group_id}")
        )
        group_data = group_response.json()
        return Group(shared=self._shared, data=group_data)

    def get_base_group(self, group_id: int) -> BaseGroup:
        """
        Gets a base group.
        FIXME
        This method does not send any requests - it just generates a BaseGroup object. Learn more about bases here.

        Arguments:
            group_id: A Roblox group ID.

        Returns:
            A BaseGroup.
        """
        return BaseGroup(shared=self._shared, group_id=group_id)

    async def get_universes(self, universe_ids: List[int]) -> List[Universe]:
        """
        Grabs a list of universes corresponding to each ID in the list.

        Arguments:
            universe_ids: A list of Roblox universe IDs.

        Returns:
            A list of Universes.
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

        Arguments:
            universe_id: A Roblox universe ID.

        Returns:
            A Universe.
        """
        universes = await self.get_universes(universe_ids=[universe_id])
        try:
            return universes[0]
        except IndexError:
            return None

    def get_base_universe(self, universe_id: int) -> BaseUniverse:
        """
        Gets a base universe.
        FIXME
        This method does not send any requests - it just generates a BaseGroup object. Learn more about bases here.

        Arguments:
            universe_id: A Roblox universe ID.

        Returns:
            A BaseUniverse.
        """
        return BaseUniverse(shared=self._shared, universe_id=universe_id)

    async def get_places(self, place_ids: List[int]) -> List[Place]:
        """
        Grabs a list of places corresponding to each ID in the list.

        Arguments:
            place_ids: A list of Roblox place IDs.

        Returns:
            A list of Places.
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

        Arguments:
            place_id: A Roblox place ID.

        Returns:
            A Place.
        """
        places = await self.get_places(place_ids=[place_id])
        try:
            return places[0]
        except IndexError:
            return None

    def get_base_place(self, place_id: int) -> BasePlace:
        """
        Gets a base place.
        FIXME
        This method does not send any requests - it just generates a BaseGroup object. Learn more about bases here.

        Arguments:
            place_id: A Roblox place ID.

        Returns:
            A BasePlace.
        """
        return BasePlace(shared=self._shared, place_id=place_id)

    async def get_asset(self, asset_id: int) -> EconomyAsset:
        """
        Gets an asset with the passed ID.

        Arguments:
            asset_id: A Roblox asset ID.

        Returns:
            An Asset.
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
        FIXME
        This method does not send any requests - it just generates a BaseGroup object. Learn more about bases here.

        Arguments:
            asset_id: A Roblox asset ID.

        Returns:
            A BaseAsset.
        """
        return BaseAsset(shared=self._shared, asset_id=asset_id)

    async def get_plugins(self, plugin_ids: List[int]) -> List[Plugin]:
        """
        Grabs a list of plugins corresponding to each ID in the list.

        Arguments:
            plugin_ids: A list of Roblox plugin IDs.

        Returns:
            A list of Plugins.
        """
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
        """
        Grabs a plugin with the passed ID.

        Arguments:
            plugin_id: A Roblox plugin ID.

        Returns:
            A Plugin.
        """
        plugins = await self.get_plugins([plugin_id])
        try:
            return plugins[0]
        except IndexError:
            return None

    def get_base_plugin(self, plugin_id: int) -> BasePlugin:
        """
        Gets a base plugin.
        FIXME
        This method does not send any requests - it just generates a BaseUser object.

        Arguments:
            plugin_id: A Roblox plugin ID.

        Returns:
            A BasePlugin.
        """
        return BasePlugin(shared=self._shared, plugin_id=plugin_id)
