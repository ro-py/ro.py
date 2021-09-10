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


class RefreshBeforeNextError(Exception):
    pass


class RetryLimitReached(Exception):
    def __init__(self, error):
        self.error = error


class PageIterator:
    """
    Represents a paginated Roblox endpoint.

    Attributes:
        _shared: The error codes
        url: url we send the request to.
        sort_order: order of the request see enum
        limit: the amount of data gotten per page
        extra_parameters: extra parameters send with the request
        item_handler: makes data in to an object
        handler_kwargs: extra kwargs for the item handler
        page_count: page we are currently at
        highest_page_count: highest page count we have reached
        previous_page_cursor: previous page cursor to get the previous page
        next_page_cursor: next page cursor to get the next page
        data: list of all data collected until now
        first: is it the first page
        max_retries: amount of times you are allowed to retry
        iterate_position: Used when iterating over the object.
        iteration_complete: Help me, please
    """

    def __init__(
            self,
            shared: ClientSharedObject,
            url: str,
            sort_order: SortOrder = SortOrder.Ascending,
            limit: int = 100,
            extra_parameters: Optional[dict] = None,
            item_handler: Callable = None,
            handler_kwargs: Optional[dict] = None,
            max_retries: int = 3
    ):
        """
        Arguments:
            shared: shared object between all objects
            url: url we are sending the request to
            sort_order: order in what we get the data back check enum
            limit: the amount of data we want to get back
            extra_parameters: extra_parameters to send with the request
            item_handler: makes json data into objects
            handler_kwargs: extra kwargs send to the item_handler function
            max_retries: amount of times you are allowed to retry
        """
        self._shared: ClientSharedObject = shared

        if handler_kwargs is None:
            handler_kwargs = {}

        self.url: str = url
        self.sort_order: SortOrder = sort_order.value
        self.limit: int = limit
        self.extra_parameters: Optional[dict] = extra_parameters
        self.item_handler: Callable = item_handler
        self.handler_kwargs: dict = handler_kwargs

        self.page_count: int = 0
        self.highest_page_count: int = 0
        self.previous_page_cursor: str = ""
        self.next_page_cursor: str = ""
        self.data: list = []
        self.first: bool = True
        self.max_retries: int = max_retries

        self.iteration_in_progress: bool = False
        self.iteration_complete: bool = False
        self.iterate_position: int = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.iteration_in_progress:
            self.iteration_in_progress = True
            await self.next()

        if self.iterate_position == len(self.data):
            try:
                await self.next()
            except NoMoreData:
                raise StopAsyncIteration

            self.iterate_position = 0

        item: dict = self.data[self.iterate_position]
        self.iterate_position += 1
        return item

    async def flatten(self):
        """
        Flattens the data into a list.

        Returns:
            data from all the pages.
        """
        while self.next_page_cursor or self.first:
            await self.next()
        return self.data

    async def _do_request(self, parameters, retries: Optional[int] = None):
        """
        Arguments:
            parameters: parameters for the request
            retries: amount of times it will ret
        """
        if retries is None:
            retries = self.max_retries
        try:
            return await self._shared.requests.get(url=self.url, params=parameters)
        except HTTPStatusError as e:
            if e.errors[0]["message"] == "InternalServerError":
                if retries <= 0:
                    raise RetryLimitReached(e)
                return await self._do_request(parameters, retries=retries - 1)
            else:
                raise e

    async def next(self) -> Union[List, dict]:
        """
        Grabs the next page of data and appends it to self.data if page has not been indexed yet.
        Raises a NoMoreData error if there is no more data.

        Returns:
            A List of objects or a dict with all the data in it if no handler is given
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

        Returns:
            A List of objects or a dict with all the data in it if no handler is given
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
