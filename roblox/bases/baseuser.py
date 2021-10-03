"""

This file contains the BaseUser object, which represents a Roblox user ID.

"""

from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING

from ..bases.baseasset import BaseAsset
from ..bases.basebadge import BaseBadge
from ..bases.basegamepass import BaseGamePass
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


class BaseUser:
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
            self, limit: int = 10, sort_order: SortOrder = SortOrder.Ascending
    ) -> PageIterator:
        """
        Grabs the user's username history.

        Returns:
            A PageIterator containing the user's username history.
        """
        return PageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url(
                "users", f"v1/users/{self.id}/username-history"
            ),
            limit=limit,
            sort_order=sort_order,
            handler=lambda shared, data: data["name"],
        )

    async def get_presence(self) -> Optional[Presence]:
        """
        Grabs the user's presence.

        Returns:
            The user's presence
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
        "but jmk,,, why is this method in the baseuser and not the client!?!?"
        That's how the API is structured. That's why.

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

        Returns: An ItemInstance, or None.
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

    async def get_asset_instance(self, asset: BaseAsset) -> Optional[AssetInstance]:
        """
        Checks if a user owns the asset, and returns details about the asset if they do.
        Returns: An AssetInstance object containing some asset details or None.
        """
        return await self.get_item_instance(
            item_type=InstanceType.asset,
            item_id=asset.id
        )

    async def get_gamepass_instance(self, gamepass: BaseGamePass) -> Optional[GamePassInstance]:
        """
        Checks if a user owns the gamepass, and returns details about the asset if they do.
        Returns: A GamePassInstance object containing some details or None.
        """
        return await self.get_item_instance(
            item_type=InstanceType.gamepass,
            item_id=gamepass.id
        )

    async def get_badge_awarded_dates(self, badges: list[BaseBadge]) -> List[PartialBadge]:
        """
        Returns:
            A list of Partial Badges containing badge awarded dates.
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
        Gets the group's roles.

        Returns: A list of the group's roles.
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

    async def get_roblox_badges(self) -> List[RobloxBadge]:
        """
        Gets the user's Roblox badges.

        Returns: A lsit of Roblox badges.
        """

        badges_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("accountinformation", f"v1/users/{self.id}/roblox-badges")
        )
        badges_data = badges_response.json()
        return [RobloxBadge(shared=self._shared, data=badge_data) for badge_data in badges_data]

    async def get_promotion_channels(self) -> UserPromotionChannels:
        """
        Gets the user's promotion channels.

        Returns: The user's promotion channels.
        """
        channels_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("accountinformation", f"v1/users/{self.id}/promotion-channels")
        )
        channels_data = channels_response.json()
        return UserPromotionChannels(
            data=channels_data
        )
