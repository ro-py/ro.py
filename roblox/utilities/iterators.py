from typing import Callable, Optional
from enum import Enum
from .shared import ClientSharedObject


class NoMoreItems(Exception):
    pass


class SortOrder(Enum):
    """
    Order in which page data should load in.
    """

    Ascending = "Asc"
    Descending = "Desc"


class PageIterator:
    """
    Represents a cursor-based, paginated Roblox object.
    For more information about how cursor-based pagination works, see https://robloxapi.wiki/wiki/Pagination.
    To use, iterate over the object with `async for`:
    ```python
    async for item in iterator:
        print(item)
    ```

    Attributes:
        _shared: The ClientSharedObject.
        url: The endpoint to hit for new page data.
        sort_order: The sort order to use for returned data.
        limit: How much data should be returned per-page.
        extra_parameters: Extra parameters to pass to the endpoint.
        handler: A callable object to use to convert raw endpoint data to parsed objects.
        handler_kwargs: Extra keyword arguments to pass to the handler.
        next_cursor: Cursor to use to advance to the next page.
        previous_cursor: Cursor to use to advance to the previous page.
        iterator_position: What position in the iterator_items the iterator is currently at.
        iterator_items: List of current items the iterator is working on.
    """

    def __init__(
            self,
            shared: ClientSharedObject,
            url: str,
            sort_order: SortOrder = SortOrder.Ascending,
            limit: int = 10,
            extra_parameters: Optional[dict] = None,
            handler: Optional[Callable] = None,
            handler_kwargs: Optional[dict] = None
    ):
        """
        Parameters:
            shared: The ClientSharedObject.
            url: The endpoint to hit for new page data.
            sort_order: The sort order to use for returned data.
            limit: How much data should be returned per-page.
            extra_parameters: Extra parameters to pass to the endpoint.
            handler: A callable object to use to convert raw endpoint data to parsed objects.
            handler_kwargs: Extra keyword arguments to pass to the handler.
        """

        self._shared: ClientSharedObject = shared

        # store some basic arguments in the object
        self.url: str = url
        self.sort_order: SortOrder = sort_order
        self.limit: int = limit

        self.extra_parameters: dict = extra_parameters or {}
        self.handler: Callable = handler
        self.handler_kwargs: dict = handler_kwargs or {}

        # cursors to use for next, previous
        self.next_cursor: str = ""
        self.previous_cursor: str = ""

        # iter values
        self.iterator_position: int = 0
        self.iterator_items: list = []
        self.next_started: bool = False

    async def next(self):
        """
        Advances the iterator to the next page.
        """
        if self.next_started and not self.next_cursor:
            # if we just started and there is no cursor
            # this is the last page, because we can go back but not forward
            # so raise the exception
            raise NoMoreItems("No more items.")

        if not self.next_started:
            self.next_started = True

        page_response = await self._shared.requests.get(
            url=self.url,
            params={
                "cursor": self.next_cursor,
                "limit": self.limit,
                "sortOrder": self.sort_order.value,
                **self.extra_parameters
            }
        )
        page_data = page_response.json()

        # fill in cursors
        self.next_cursor = page_data["nextPageCursor"]
        self.previous_cursor = page_data["previousPageCursor"]

        data = page_data["data"]

        if self.handler:
            data = [
                self.handler(
                    shared=self._shared,
                    data=item_data,
                    **self.handler_kwargs
                ) for item_data in data
            ]

        return data

    async def flatten(self) -> list:
        """
        Flattens the data into a list.
        """
        items: list = []

        while True:
            try:
                new_items = await self.next()
                items += new_items
            except NoMoreItems:
                break

        return items

    def __aiter__(self):
        self.iterator_position = 0
        self.iterator_items = []
        return self

    async def __anext__(self):
        if self.iterator_position == len(self.iterator_items):
            # we are at the end of our current page of items. start again with a new page
            self.iterator_position = 0
            try:
                # get new items
                self.iterator_items = await self.next()
            except NoMoreItems:
                # if there aren't any more items, reset and break the loop
                self.iterator_position = 0
                self.iterator_items = []
                raise StopAsyncIteration

        # if we got here we know there are more items
        try:
            item = self.iterator_items[self.iterator_position]
        except IndexError:
            # edge case for group roles
            raise StopAsyncIteration
        # we advance the iterator by one for the next iteration
        self.iterator_position += 1
        return item
