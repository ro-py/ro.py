from typing import Callable
from enum import Enum

from .shared import ClientSharedObject


class SortOrder(Enum):
    """
    Order in which page data should load in.
    """

    Ascending = "Asc"
    Descending = "Desc"


class NoMoreData(Exception):
    pass


class PageIterator:
    """
    Represents a paginated Roblox endpoint.
    """

    def __init__(
        self,
        shared: ClientSharedObject,
        url: str,
        sort_order: SortOrder = SortOrder.Ascending,
        limit: int = 10,
        extra_parameters: dict = None,
        item_handler: Callable = None,
        handler_kwargs: dict = None
    ):
        self._shared: ClientSharedObject = shared

        if handler_kwargs is None:
            handler_kwargs = {}

        self.url: str = url
        self.sort_order: SortOrder = sort_order.value
        self.limit: int = limit
        self.extra_parameters: dict = extra_parameters
        self.item_handler: Callable = item_handler
        self.handler_kwargs: dict = handler_kwargs

        self.previous_page_cursor: str = ""
        self.next_page_cursor: str = ""
        self.more_data: bool = True

        self.data: list = []

    async def flatten(self):
        """
        Flattens the data into a list.
        """

        while self.more_data:
            await self.next()
        return self.data

    async def next(self):
        """
        Grabs the next page of data and appends it to self.data.
        Raises a NoMoreData error if there is no more data.
        """

        if not self.more_data:
            raise NoMoreData("No more data.")

        parameters = {
            "cursor": self.next_page_cursor,
            "limit": self.limit,
            "sortOrder": self.sort_order,
        }

        if self.extra_parameters:
            parameters.update(self.extra_parameters)

        page_response = await self._shared.requests.get(url=self.url, params=parameters)
        page_data = page_response.json()

        self.next_page_cursor = page_data["nextPageCursor"]
        self.previous_page_cursor = page_data["previousPageCursor"]
        if self.item_handler:
            self.data += [
                self.item_handler(
                    shared=self._shared,
                    data=item_data,
                    **self.handler_kwargs
                ) for item_data in page_data["data"]
            ]
        else:
            self.data += page_data["data"]

        if not self.next_page_cursor:
            self.more_data = False
