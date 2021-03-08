import iso8601


class Presence:
    def __init__(self, cso, user, data):
        self.cso = cso
        self.requests = cso.requests

        self.user = user
        self.user_presence_type = data["userPresenceType"]
        self.place_id = data["placeId"]
        self.root_place_id = data["rootPlaceId"]
        self.game_id = data["gameId"]
        self.universe_id = data["universeId"]
        self.last_location = data["lastLocation"]
        self.last_online = iso8601.parse_date(data["lastOnline"])

    async def get_game(self):
        if self.universe_id:
            return await self.cso.client.get_game_by_universe_id(self.universe_id)
        else:
            return None
