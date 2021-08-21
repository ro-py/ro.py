from ..utilities.shared import ClientSharedObject


class BaseUser:
    def __init__(self, shared: ClientSharedObject, user_id: int):
        self._shared = shared
        self.id: int = user_id

    async def get_status(self):
        status_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("users", f"/v1/users/{self.id}/status")
        )
        status_data = status_response.json()
        return status_data["status"]
