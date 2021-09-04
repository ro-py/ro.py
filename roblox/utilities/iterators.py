from typing import Callable, List, Union, Optional
from enum import Enum

from .shared import ClientSharedObject
from ..utilities.exceptions import HTTPStatusError


class SortOrder(Enum):
    """
    Order in which page data should load in.
    """

    Ascending = "Asc"
    Descending = "Desc"


class NoMoreData(Exception):
    pass


class RetryLimitReached(Exception):
    def __init__(self, error):
        self.error = error


class PageIterator:
    """
    Represents a paginated Roblox endpoint.
    """

    def __init__(
            self,
            shared: ClientSharedObject,
            url: str,
            sort_order: SortOrder = SortOrder.Ascending,
            limit: int = 100,
            extra_parameters: dict = None,
            item_handler: Callable = None,
            handler_kwargs: dict = None,
            max_retires: int = 3
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

        self.page_count = 0
        self.highest_page_count = 0
        self.previous_page_cursor: str = ""
        self.next_page_cursor: str = ""
        self.data: list = []
        self.first = True
        self.max_retires: int = max_retires

    async def flatten(self):
        """
        Flattens the data into a list.
        """
        while self.next_page_cursor or self.first:
            await self.next()
        return self.data

    async def _do_request(self, parameters, retires: Optional[int] = None):
        if retires is None:
            retires = self.max_retires
        try:
            return await self._shared.requests.get(url=self.url, params=parameters)
        except HTTPStatusError as e:
            if e.errors[0]["message"] == "InternalServerError":
                if retires <= 0:
                    raise RetryLimitReached(e)
                return await self._do_request(parameters, retires=retires - 1)
            else:
                raise e

    async def next(self) -> Union[List, dict]:
        """
        Grabs the next page of data and appends it to self.data if page has not been indexed yet.
        Raises a NoMoreData error if there is no more data.

        Returns:

        """

        if not self.next_page_cursor and not self.first:
            raise NoMoreData("No more data.")
        self.first = False
        self.page_count += 1
        parameters = {
            "cursor": self.next_page_cursor,
            "limit": self.limit,
            "sortOrder": self.sort_order,
        }
        if self.extra_parameters:
            parameters.update(self.extra_parameters)

        page_response = await self._do_request(parameters)
        page_data = page_response.json()
        self.next_page_cursor = page_data["nextPageCursor"]
        self.previous_page_cursor = page_data["previousPageCursor"]
        if self.item_handler:
            current_data = [
                self.item_handler(
                    shared=self._shared,
                    data=item_data,
                    **self.handler_kwargs
                ) for item_data in page_data["data"]
            ]
        else:
            current_data = page_data["data"]
        if self.page_count > self.highest_page_count:
            self.highest_page_count = self.page_count
            self.data = self.data + current_data

        return current_data

    async def previous(self) -> Union[List, dict]:
        """
        Grabs the previous page of data and appends it to self.data.
        Raises a NoMoreData error if there is no more data.
        """
        if not self.previous_page_cursor:
            raise NoMoreData("No more data.")
        self.page_count -= 1
        parameters = {
            "cursor": self.previous_page_cursor,
            "limit": self.limit,
            "sortOrder": self.sort_order,
        }

        if self.extra_parameters:
            parameters.update(self.extra_parameters)

        page_response = await self._do_request(parameters)
        page_data = page_response.json()
        self.next_page_cursor = page_data["nextPageCursor"]
        self.previous_page_cursor = page_data["previousPageCursor"]
        if self.item_handler:
            current_data = [
                self.item_handler(
                    shared=self._shared,
                    data=item_data,
                    **self.handler_kwargs
                ) for item_data in page_data["data"]
            ]
        else:
            current_data = page_data["data"]

        return current_data
