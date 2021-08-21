from ..utilities.shared import ClientSharedObject
from ..utilities.iterators import PageIterator, SortOrder


class BaseUser:
    def __init__(self, shared: ClientSharedObject, user_id: int):
        self._shared: ClientSharedObject = shared
        self.id: int = user_id

    async def get_status(self):
        status_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("users", f"/v1/users/{self.id}/status")
        )
        status_data = status_response.json()
        return status_data["status"]

    def username_history(self, limit: int = 10, sort_order: SortOrder = SortOrder.Ascending) -> PageIterator:
        return PageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url("users", f"v1/users/{self.id}/username-history"),
            limit=limit,
            item_handler=lambda data: data["name"]
        )
