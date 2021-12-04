"""

This file contains the BaseUser object, which represents a Roblox user ID.

"""

from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING

from .baseitem import BaseItem
from ..bases.basebadge import BaseBadge
from ..instances import ItemInstance, InstanceType, AssetInstance, GamePassInstance, instance_classes
from ..partials.partialbadge import PartialBadge
from ..presence import Presence
from ..promotionchannels import UserPromotionChannels
from ..robloxbadges import RobloxBadge
from ..utilities.iterators import PageIterator, SortOrder
from ..utilities.shared import ClientSharedObject

if TYPE_CHECKING:
    from ..friends import Friend
    from ..roles import Role
    from ..utilities.types import AssetOrAssetId, GamePassOrGamePassId


class BaseUser(BaseItem):
    """
    Represents a Roblox user ID.

    Attributes:
        _shared: The ClientSharedObject.
        id: The user ID.
    """

    def __init__(self, shared: ClientSharedObject, user_id: int):
        """
        Arguments:
            shared: The ClientSharedObject.
            user_id: The user ID.
        """

        self._shared: ClientSharedObject = shared
        self.id: int = user_id

    async def get_status(self) -> str:
        """
        Grabs the user's status.

        Returns:
            The user's status.
        """
        status_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url(
                "users", f"/v1/users/{self.id}/status"
            )
        )
        status_data = status_response.json()
        return status_data["status"]

    def username_history(
            self, page_size: int = 10, sort_order: SortOrder = SortOrder.Ascending, max_items: int = None
    ) -> PageIterator:
        """
        Grabs the user's username history.

        Arguments:
            page_size: How many members should be returned for each page.
            sort_order: Order in which data should be grabbed.
            max_items: The maximum items to return when looping through this object.

        Returns:
            A PageIterator containing the user's username history.
        """
        return PageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url(
                "users", f"v1/users/{self.id}/username-history"
            ),
            page_size=page_size,
            sort_order=sort_order,
            max_items=max_items,
            handler=lambda shared, data: data["name"],
        )

    async def get_presence(self) -> Optional[Presence]:
        """
        Grabs the user's presence.

        Returns:
            The user's presence, if they have an active presence.
        """
        presences = await self._shared.presence_provider.get_user_presences([self.id])
        try:
            return presences[0]
        except IndexError:
            return None

    async def get_friends(self) -> List[Friend]:
        """
        Grabs the user's friends.

        Returns:
            A list of the user's friends.
        """

        from ..friends import Friend
        friends_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("friends", f"v1/users/{self.id}/friends")
        )
        friends_data = friends_response.json()["data"]
        return [Friend(shared=self._shared, data=friend_data) for friend_data in friends_data]

    async def get_currency(self) -> int:
        """
        Grabs the user's current Robux amount. Only works on the authenticated user.

        Returns:
            The user's Robux amount.
        """
        currency_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("economy", f"v1/users/{self.id}/currency")
        )
        currency_data = currency_response.json()
        return currency_data["robux"]

    async def has_premium(self) -> bool:
        """
        Checks if the user has a Roblox Premium membership.

        Returns:
            Whether the user has Premium or not.
        """
        premium_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("premiumfeatures", f"v1/users/{self.id}/validate-membership")
        )
        premium_data = premium_response.text
        return premium_data == "true"

    async def get_item_instance(self, item_type: InstanceType, item_id: int) -> Optional[ItemInstance]:
        """
        Gets an item instance for a specific user.

        Arguments:
            item_type: The type of item to get an instance for.
            item_id: The item's ID.

        Returns: An ItemInstance, if it exists.
        """

        item_type: str = item_type.value.lower()

        # this is so we can have special classes for other types
        item_class = instance_classes.get(item_type) or ItemInstance

        instance_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("inventory", f"v1/users/{self.id}/items/{item_type}/{item_id}")
        )
        instance_data = instance_response.json()["data"]
        if len(instance_data) > 0:
            return item_class(
                shared=self._shared,
                data=instance_data[0]
            )
        else:
            return None

    async def get_asset_instance(self, asset: AssetOrAssetId) -> Optional[AssetInstance]:
        """
        Checks if a user owns the asset, and returns details about the asset if they do.

        Returns:
            An asset instance, if the user owns this asset.
        """
        return await self.get_item_instance(
            item_type=InstanceType.asset,
            item_id=int(asset)
        )

    async def get_gamepass_instance(self, gamepass: GamePassOrGamePassId) -> Optional[GamePassInstance]:
        """
        Checks if a user owns the gamepass, and returns details about the asset if they do.

        Returns:
            An gamepass instance, if the user owns this gamepass.
        """
        return await self.get_item_instance(
            item_type=InstanceType.gamepass,
            item_id=int(gamepass)
        )

    async def get_badge_awarded_dates(self, badges: list[BaseBadge]) -> List[PartialBadge]:
        """
        Gets the dates that each badge in a list of badges were awarded to this user.

        Returns:
            A list of partial badges containing badge awarded dates.
        """
        awarded_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("badges", f"v1/users/{self.id}/badges/awarded-dates"),
            params={
                "badgeIds": [badge.id for badge in badges]
            }
        )
        awarded_data: list = awarded_response.json()["data"]
        return [
            PartialBadge(
                shared=self._shared,
                data=partial_data
            ) for partial_data in awarded_data
        ]

    async def get_group_roles(self) -> List[Role]:
        """
        Gets a list of roles for all groups this user is in.

        Returns:
            A list of roles.
        """
        from ..roles import Role
        from ..groups import Group
        roles_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("groups", f"v1/users/{self.id}/groups/roles")
        )
        roles_data = roles_response.json()["data"]
        return [
            Role(
                shared=self._shared,
                data=role_data["role"],
                group=Group(
                    shared=self._shared,
                    data=role_data["group"]
                )
            ) for role_data in roles_data
        ]

    async def get_primary_group_role(self) -> Optional[Role]:
        """
        Gets a role for the primary group this user is in.

        Returns:
            Role
        """
        from ..roles import Role
        from ..groups import Group
        roles_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("groups", f"v1/users/{self.id}/groups/primary/role")
        )
        json = roles_response.json()
        if json is None:
            return None
        return Role(
                shared=self._shared,
                data=json["role"],
                group=Group(
                    shared=self._shared,
                    data=json["group"]
                )
            )

    async def get_roblox_badges(self) -> List[RobloxBadge]:
        """
        Gets the user's Roblox badges.

        Returns:
            A list of Roblox badges.
        """

        badges_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("accountinformation", f"v1/users/{self.id}/roblox-badges")
        )
        badges_data = badges_response.json()
        return [RobloxBadge(shared=self._shared, data=badge_data) for badge_data in badges_data]

    async def get_promotion_channels(self) -> UserPromotionChannels:
        """
        Gets the user's promotion channels.

        Returns:
            The user's promotion channels.
        """
        channels_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("accountinformation", f"v1/users/{self.id}/promotion-channels")
        )
        channels_data = channels_response.json()
        return UserPromotionChannels(
            data=channels_data
        )

    async def _get_friend_channel_count(self, channel: str) -> int:
        count_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("friends", f"v1/users/{self.id}/{channel}/count")
        )
        return count_response.json()["count"]

    def _get_friend_channel_iterator(
            self,
            channel: str,
            page_size: int = 10,
            sort_order: SortOrder = SortOrder.Ascending, max_items: int = None
    ) -> PageIterator:
        from ..friends import Friend
        return PageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url("friends", f"v1/users/{self.id}/{channel}"),
            page_size=page_size,
            sort_order=sort_order,
            max_items=max_items,
            handler=lambda shared, data: Friend(shared=shared, data=data)
        )

    async def get_friend_count(self) -> int:
        """
        Gets the user's friend count.

        Returns:
            The user's friend count.
        """
        return await self._get_friend_channel_count("friends")

    async def get_follower_count(self) -> int:
        """
        Gets the user's follower count.

        Returns:
            The user's follower count.
        """
        return await self._get_friend_channel_count("followers")

    async def get_following_count(self) -> int:
        """
        Gets the user's following count.

        Returns:
            The user's following count.
        """
        return await self._get_friend_channel_count("followings")

    def get_followers(
            self,
            page_size: int = 10,
            sort_order: SortOrder = SortOrder.Ascending, max_items: int = None
    ) -> PageIterator:
        """
        Gets the user's followers.

        Returns:
            A PageIterator containing everyone who follows this user.
        """
        return self._get_friend_channel_iterator(
            channel="followers",
            page_size=page_size,
            sort_order=sort_order,
            max_items=max_items,
        )

    def get_followings(
            self,
            page_size: int = 10,
            sort_order: SortOrder = SortOrder.Ascending, max_items: int = None
    ) -> PageIterator:
        """
        Gets the user's followings.

        Returns:
            A PageIterator containing everyone that this user is following.
        """
        return self._get_friend_channel_iterator(
            channel="followings",
            page_size=page_size,
            sort_order=sort_order,
            max_items=max_items,
        )
