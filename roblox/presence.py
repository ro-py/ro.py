from typing import Optional
from datetime import datetime
from dateutil.parser import parse

from .utilities.shared import ClientSharedObject

from .bases.baseuniverse import BaseUniverse
from .bases.baseplace import BasePlace


class Presence:
    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared
        self._data: dict = data

        self.user_presence_type: int = data["userPresenceType"]
        self.last_location: str = data["lastLocation"]

        self.place: Optional[BasePlace] = data.get("placeId") and BasePlace(
            shared=shared, place_id=data["placeId"]
        )

        self.root_place: Optional[BasePlace] = data.get("rootPlaceId") and BasePlace(
            shared=shared, place_id=data["rootPlaceId"]
        )

        self.game_id: Optional[str] = data["gameId"]

        self.universe: Optional[BaseUniverse] = data.get("universeId") and BaseUniverse(
            shared=shared, universe_id=data["universeId"]
        )

        self.user_id: int = data["userId"]
        self.last_online: datetime = parse(data["lastOnline"])


class PresenceProvider:
    def __init__(self, shared: ClientSharedObject):
        self._shared: ClientSharedObject = shared

    async def get_user_presences(self, user_ids: list[int]) -> list[Presence]:
        """
        Returns a list of Presence objects corresponding to each user in the list.
        """
        presences_response = await self._shared.requests.post(
            url=self._shared.url_generator.get_url("presence", "v1/presence/users"),
            json={"userIds": user_ids},
        )
        presences_data = presences_response.json()["userPresences"]
        return [
            Presence(shared=self._shared, data=presence_data)
            for presence_data in presences_data
        ]
