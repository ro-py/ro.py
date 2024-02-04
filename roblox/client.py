"""

Contains the Client, which is the core object at the center of all ro.py applications.

"""

from typing import Union, List, Optional

from .account import AccountProvider
from .assets import EconomyAsset
from .badges import Badge
from .bases.baseasset import BaseAsset
from .bases.basebadge import BaseBadge
from .bases.basegamepass import BaseGamePass
from .bases.basegroup import BaseGroup
from .bases.baseplace import BasePlace
from .bases.baseplugin import BasePlugin
from .bases.baseuniverse import BaseUniverse
from .bases.baseuser import BaseUser
from .chat import ChatProvider
from .delivery import DeliveryProvider
from .groups import Group
from .partials.partialuser import PartialUser, RequestedUsernamePartialUser, PreviousUsernamesPartialUser
from .places import Place
from .plugins import Plugin
from .presence import PresenceProvider
from .thumbnails import ThumbnailProvider
from .universes import Universe
from .users import User
from .utilities.exceptions import BadRequest, NotFound, AssetNotFound, BadgeNotFound, GroupNotFound, PlaceNotFound, \
    PluginNotFound, UniverseNotFound, UserNotFound
from .utilities.iterators import PageIterator
from .utilities.requests import Requests
from .utilities.url import URLGenerator


class Client:
    """
    Represents a Roblox client.

    Attributes:
        requests: The requests object, which is used to send requests to Roblox endpoints.
        url_generator: The URL generator object, which is used to generate URLs to send requests to endpoints.
        presence: The presence provider object.
        thumbnails: The thumbnail provider object.
        delivery: The delivery provider object.
        chat: The chat provider object.
        account: The account provider object.
    """

    def __init__(self, token: str = None, base_url: str = "roblox.com"):
        """
        Arguments:
            token: A .ROBLOSECURITY token to authenticate the client with.
            base_url: The base URL to use when sending requests.
        """
        self._url_generator: URLGenerator = URLGenerator(base_url=base_url)
        self._requests: Requests = Requests()

        self.url_generator: URLGenerator = self._url_generator
        self.requests: Requests = self._requests

        self.presence: PresenceProvider = PresenceProvider(client=self)
        self.thumbnails: ThumbnailProvider = ThumbnailProvider(client=self)
        self.delivery: DeliveryProvider = DeliveryProvider(client=self)
        self.chat: ChatProvider = ChatProvider(client=self)
        self.account: AccountProvider = AccountProvider(client=self)

        if token:
            self.set_token(token)

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    # Authentication
    def set_token(self, token: Optional[str] = None) -> None:
        """
        Authenticates the client with the passed .ROBLOSECURITY token.
        This method does not send any requests and will not throw if the token is invalid.

        Arguments:
            token: A .ROBLOSECURITY token to authenticate the client with.

        """
        self._requests.session.cookies[".ROBLOSECURITY"] = token

    # Users
    async def get_user(self, user_id: int) -> User:
        """
        Gets a user with the specified user ID.

        Arguments:
            user_id: A Roblox user ID.

        Returns:
            A user object.
        """
        try:
            user_response = await self._requests.get(
                url=self.url_generator.get_url("users", f"v1/users/{user_id}")
            )
        except NotFound as exception:
            raise UserNotFound(
                message="Invalid user.",
                response=exception.response
            ) from None
        user_data = user_response.json()
        return User(client=self, data=user_data)

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
            url=self._url_generator.get_url("users", f"v1/users/authenticated")
        )
        authenticated_user_data = authenticated_user_response.json()

        if expand:
            return await self.get_user(authenticated_user_data["id"])
        else:
            return PartialUser(client=self, data=authenticated_user_data)

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
            url=self._url_generator.get_url("users", f"v1/users"),
            json={"userIds": user_ids, "excludeBannedUsers": exclude_banned_users},
        )
        users_data = users_response.json()["data"]

        if expand:
            return [await self.get_user(user_data["id"]) for user_data in users_data]
        else:
            return [
                PartialUser(client=self, data=user_data)
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
            url=self._url_generator.get_url("users", f"v1/usernames/users"),
            json={"usernames": usernames, "excludeBannedUsers": exclude_banned_users},
        )
        users_data = users_response.json()["data"]

        if expand:
            return [await self.get_user(user_data["id"]) for user_data in users_data]
        else:
            return [
                RequestedUsernamePartialUser(client=self, data=user_data)
                for user_data in users_data
            ]

    async def get_user_by_username(
            self, username: str, exclude_banned_users: bool = False, expand: bool = True
    ) -> Union[RequestedUsernamePartialUser, User]:
        """
        Grabs a user corresponding to the passed username.

        Arguments:
            username: A Roblox username.
            exclude_banned_users: Whether to exclude banned users from the data.
            expand: Whether to return a User (2 requests) rather than a RequestedUsernamePartialUser (1 request)

        Returns:
            A User or RequestedUsernamePartialUser depending on the expand argument.
        """
        users = await self.get_users_by_usernames(
            usernames=[username],
            exclude_banned_users=exclude_banned_users,
            expand=expand,
        )
        try:
            return users[0]
        except IndexError:
            raise UserNotFound("Invalid username.") from None

    def get_base_user(self, user_id: int) -> BaseUser:
        """
        Gets a base user.

        !!! note
            This method does not send any requests - it just generates an object.
            For more information on bases, please see [Bases](../tutorials/bases.md).

        Arguments:
            user_id: A Roblox user ID.

        Returns:
            A BaseUser.
        """
        return BaseUser(client=self, user_id=user_id)

    def user_search(self, keyword: str, page_size: int = 10,
                    max_items: int = None) -> PageIterator:
        """
        Search for users with a keyword.

        Arguments:
            keyword: A keyword to search for.
            page_size: How many members should be returned for each page.
            max_items: The maximum items to return when looping through this object.

        Returns:
            A PageIterator containing RequestedUsernamePartialUser.
        """
        return PageIterator(
            client=self,
            url=self._url_generator.get_url("users", f"v1/users/search"),
            page_size=page_size,
            max_items=max_items,
            extra_parameters={"keyword": keyword},
            handler=lambda client, data: PreviousUsernamesPartialUser(client=client, data=data),
        )

    # Groups
    async def get_group(self, group_id: int) -> Group:
        """
        Gets a group by its ID.

        Arguments:
            group_id: A Roblox group ID.

        Returns:
            A Group.
        """
        try:
            group_response = await self._requests.get(
                url=self._url_generator.get_url("groups", f"v1/groups/{group_id}")
            )
        except BadRequest as exception:
            raise GroupNotFound(
                message="Invalid group.",
                response=exception.response
            ) from None
        group_data = group_response.json()
        return Group(client=self, data=group_data)

    def get_base_group(self, group_id: int) -> BaseGroup:
        """
        Gets a base group.

        !!! note
            This method does not send any requests - it just generates an object.
            For more information on bases, please see [Bases](../tutorials/bases.md).

        Arguments:
            group_id: A Roblox group ID.

        Returns:
            A BaseGroup.
        """
        return BaseGroup(client=self, group_id=group_id)

    # Universes
    async def get_universes(self, universe_ids: List[int]) -> List[Universe]:
        """
        Grabs a list of universes corresponding to each ID in the list.

        Arguments:
            universe_ids: A list of Roblox universe IDs.

        Returns:
            A list of Universes.
        """
        universes_response = await self._requests.get(
            url=self._url_generator.get_url("games", "v1/games"),
            params={"universeIds": universe_ids},
        )
        universes_data = universes_response.json()["data"]
        return [
            Universe(client=self, data=universe_data)
            for universe_data in universes_data
        ]

    async def get_universe(self, universe_id: int) -> Universe:
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
            raise UniverseNotFound("Invalid universe.") from None

    def get_base_universe(self, universe_id: int) -> BaseUniverse:
        """
        Gets a base universe.

        !!! note
            This method does not send any requests - it just generates an object.
            For more information on bases, please see [Bases](../tutorials/bases.md).

        Arguments:
            universe_id: A Roblox universe ID.

        Returns:
            A BaseUniverse.
        """
        return BaseUniverse(client=self, universe_id=universe_id)

    # Places
    async def get_places(self, place_ids: List[int]) -> List[Place]:
        """
        Grabs a list of places corresponding to each ID in the list.

        Arguments:
            place_ids: A list of Roblox place IDs.

        Returns:
            A list of Places.
        """
        places_response = await self._requests.get(
            url=self._url_generator.get_url(
                "games", f"v1/games/multiget-place-details"
            ),
            params={"placeIds": place_ids},
        )
        places_data = places_response.json()
        return [
            Place(client=self, data=place_data) for place_data in places_data
        ]

    async def get_place(self, place_id: int) -> Place:
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
            raise PlaceNotFound("Invalid place.") from None

    def get_base_place(self, place_id: int) -> BasePlace:
        """
        Gets a base place.

        !!! note
            This method does not send any requests - it just generates an object.
            For more information on bases, please see [Bases](../tutorials/bases.md).

        Arguments:
            place_id: A Roblox place ID.

        Returns:
            A BasePlace.
        """
        return BasePlace(client=self, place_id=place_id)

    # Assets
    async def get_asset(self, asset_id: int) -> EconomyAsset:
        """
        Gets an asset with the passed ID.

        Arguments:
            asset_id: A Roblox asset ID.

        Returns:
            An Asset.
        """
        try:
            asset_response = await self._requests.get(
                url=self._url_generator.get_url(
                    "economy", f"v2/assets/{asset_id}/details"
                )
            )
        except BadRequest as exception:
            raise AssetNotFound(
                message="Invalid asset.",
                response=exception.response
            ) from None
        asset_data = asset_response.json()
        return EconomyAsset(client=self, data=asset_data)

    def get_base_asset(self, asset_id: int) -> BaseAsset:
        """
        Gets a base asset.

        !!! note
            This method does not send any requests - it just generates an object.
            For more information on bases, please see [Bases](../tutorials/bases.md).

        Arguments:
            asset_id: A Roblox asset ID.

        Returns:
            A BaseAsset.
        """
        return BaseAsset(client=self, asset_id=asset_id)

    # Plugins
    async def get_plugins(self, plugin_ids: List[int]) -> List[Plugin]:
        """
        Grabs a list of plugins corresponding to each ID in the list.

        Arguments:
            plugin_ids: A list of Roblox plugin IDs.

        Returns:
            A list of Plugins.
        """
        plugins_response = await self._requests.get(
            url=self._url_generator.get_url(
                "develop", "v1/plugins"
            ),
            params={
                "pluginIds": plugin_ids
            }
        )
        plugins_data = plugins_response.json()["data"]
        return [Plugin(client=self, data=plugin_data) for plugin_data in plugins_data]

    async def get_plugin(self, plugin_id: int) -> Plugin:
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
            raise PluginNotFound("Invalid plugin.") from None

    def get_base_plugin(self, plugin_id: int) -> BasePlugin:
        """
        Gets a base plugin.

        !!! note
            This method does not send any requests - it just generates an object.
            For more information on bases, please see [Bases](../tutorials/bases.md).

        Arguments:
            plugin_id: A Roblox plugin ID.

        Returns:
            A BasePlugin.
        """
        return BasePlugin(client=self, plugin_id=plugin_id)

    # Badges
    async def get_badge(self, badge_id: int) -> Badge:
        """
        Gets a badge with the passed ID.

        Arguments:
            badge_id: A Roblox badge ID.

        Returns:
            A Badge.
        """
        try:
            badge_response = await self._requests.get(
                url=self._url_generator.get_url(
                    "badges", f"v1/badges/{badge_id}"
                )
            )
        except NotFound as exception:
            raise BadgeNotFound(
                message="Invalid badge.",
                response=exception.response
            ) from None
        badge_data = badge_response.json()
        return Badge(client=self, data=badge_data)

    def get_base_badge(self, badge_id: int) -> BaseBadge:
        """
        Gets a base badge.

        !!! note
            This method does not send any requests - it just generates an object.
            For more information on bases, please see [Bases](../tutorials/bases.md).

        Arguments:
            badge_id: A Roblox badge ID.

        Returns:
            A BaseBadge.
        """
        return BaseBadge(client=self, badge_id=badge_id)

    # Gamepasses
    def get_base_gamepass(self, gamepass_id: int) -> BaseGamePass:
        """
        Gets a base gamepass.

        !!! note
            This method does not send any requests - it just generates an object.
            For more information on bases, please see [Bases](../tutorials/bases.md).

        Arguments:
            gamepass_id: A Roblox gamepass ID.

        Returns: A BaseGamePass.
        """
        return BaseGamePass(client=self, gamepass_id=gamepass_id)
