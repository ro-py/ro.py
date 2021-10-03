from datetime import datetime
from typing import Optional, List

from dateutil.parser import parse

from .bases.baseplace import BasePlace
from .bases.baseuniverse import BaseUniverse
from .utilities.shared import ClientSharedObject


class Presence:
    """
    The PresenceProvider is an object that represents https://presence.roblox.com/ and provides multiple functions
    for fetching user presence information.

    Attributes:
        _shared: The shared object, which is passed to all objects this client generates.
        _data: The data form the request.
        user_presence_type: type of presence?
        last_location: last location the user visited.
        place: place of the last visited game.
        root_place: root_place of the last visited game.
        game_id: game_id of the last visited game.
        universe: universe of the last visited game.
        user_id: the id of the currently selected user.
        last_online: when that user was online for the last time.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: Shared object.
            data: The data form the request.
        """
        self._shared: ClientSharedObject = shared
        self._data: dict = data

        self.user_presence_type: int = data["userPresenceType"]
        self.last_location: str = data["lastLocation"]

        self.place: Optional[BasePlace] = data.get("placeId") and BasePlace(
            shared=shared,
            place_id=data["placeId"]
        )

        self.root_place: Optional[BasePlace] = data.get("rootPlaceId") and BasePlace(
            shared=shared,
            place_id=data["rootPlaceId"]
        )

        self.game_id: Optional[str] = data["gameId"]

        self.universe: Optional[BaseUniverse] = data.get("universeId") and BaseUniverse(
            shared=shared,
            universe_id=data["universeId"]
        )

        self.user_id: int = data["userId"]
        self.last_online: datetime = parse(data["lastOnline"])


class PresenceProvider:
    """
    The PresenceProvider provides multiple functions for fetching user presence information.

    Attributes:
        _shared: The shared object, which is passed to all objects this client generates.
    """

    def __init__(self, shared: ClientSharedObject):
        self._shared: ClientSharedObject = shared

    async def get_user_presences(self, user_ids: List[int]) -> List[Presence]:
        """
        Returns a list of Presence objects corresponding to each user in the list.

        Arguments:
            user_ids: The list of users you want to presences form.

        Returns:
            A List of Presence.
        """

        presences_response = await self._shared.requests.post(
            url=self._shared.url_generator.get_url("presence", "v1/presence/users"),
            json={
                "userIds": user_ids
            }
        )
        presences_data = presences_response.json()["userPresences"]
        return [Presence(shared=self._shared, data=presence_data) for presence_data in presences_data]
