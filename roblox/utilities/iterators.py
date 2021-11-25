"""

This module contains iterators used internally by ro.py to provide paginated information.

"""

from __future__ import annotations

from enum import Enum
from typing import Callable, Optional, AsyncIterator

from .exceptions import NoMoreItems
from .shared import ClientSharedObject


class SortOrder(Enum):
    """
    Order in which page data should load in.
    """

    Ascending = "Asc"
    Descending = "Desc"


class IteratorItems(AsyncIterator):
    """
    Represents the items inside of an iterator.
    """

    def __init__(self, iterator: RobloxIterator, max_items: Optional[int] = None):
        self._iterator = iterator
        self._position: int = 0
        self._global_position: int = 0
        self._items: list = []
        self._max_items = max_items

    def __aiter__(self):
        self._position = 0
        self._items = []
        return self

    async def __anext__(self):
        if self._position == len(self._items):
            # we are at the end of our current page of items. start again with a new page
            self._position = 0
            try:
                # get new items
                self._items = await self._iterator.next()
            except NoMoreItems:
                # if there aren't any more items, reset and break the loop
                self._position = 0
                self._global_position = 0
                self._items = []
                raise StopAsyncIteration

        if self._max_items is not None and self._global_position >= self._max_items:
            raise StopAsyncIteration

        # if we got here we know there are more items
        try:
            item = self._items[self._position]
        except IndexError:
            # edge case for group roles
            raise StopAsyncIteration
        # we advance the iterator by one for the next iteration
        self._position += 1
        self._global_position += 1
        return item


class IteratorPages(AsyncIterator):
    """
    Represents the pages inside of an iterator.
    """

    def __init__(self, iterator: RobloxIterator):
        self._iterator = iterator

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            page = await self._iterator.next()
            return page
        except NoMoreItems:
            raise StopAsyncIteration


class RobloxIterator:
    """
    Represents a basic iterator which all iterators should implement.
    """

    def __init__(self, max_items: int = None):
        self.max_items: Optional[int] = max_items

    async def next(self):
        """
        Moves to the next page and returns that page's data.
        """

        raise NotImplementedError

    async def flatten(self, max_items: int = None) -> list:
        """
        Flattens the data into a list.
        """
        if max_items is None:
            max_items = self.max_items

        items: list = []

        while True:
            try:
                new_items = await self.next()
                items += new_items
            except NoMoreItems:
                break

            if max_items is not None and len(items) >= max_items:
                break

        return items[:max_items]

    def __aiter__(self):
        return IteratorItems(
            iterator=self,
            max_items=self.max_items
        )

    def items(self, max_items: int = None) -> IteratorItems:
        """
        Returns an AsyncIterable containing each iterator item.
        """
        if max_items is None:
            max_items = self.max_items
        return IteratorItems(
            iterator=self,
            max_items=max_items
        )

    def pages(self) -> IteratorPages:
        """
        Returns an AsyncIterable containing each iterator page. Each page is a list of items.
        """
        return IteratorPages(self)


class PageIterator(RobloxIterator):
    """
    Represents a cursor-based, paginated Roblox object. Learn more about iterators in the pagination tutorial:
    [Pagination](/tutorial/pagination)
    For more information about how cursor-based pagination works, see https://robloxapi.wiki/wiki/Pagination.

    Attributes:
        _shared: The ClientSharedObject.
        url: The endpoint to hit for new page data.
        sort_order: The sort order to use for returned data.
        page_size: How much data should be returned per-page.
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
            page_size: int = 10,
            max_items: int = None,
            extra_parameters: Optional[dict] = None,
            handler: Optional[Callable] = None,
            handler_kwargs: Optional[dict] = None
    ):
        """
        Parameters:
            shared: The ClientSharedObject.
            url: The endpoint to hit for new page data.
            sort_order: The sort order to use for returned data.
            page_size: How much data should be returned per-page.
            max_items: The maximum amount of items to return when this iterator is looped through.
            extra_parameters: Extra parameters to pass to the endpoint.
            handler: A callable object to use to convert raw endpoint data to parsed objects.
            handler_kwargs: Extra keyword arguments to pass to the handler.
        """
        super().__init__(max_items=max_items)

        self._shared: ClientSharedObject = shared

        # store some basic arguments in the object
        self.url: str = url
        self.sort_order: SortOrder = sort_order
        self.page_size: int = page_size

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
            """
            If we just started and there is no cursor, this is the last page, because we can go back but not forward.
            We should raise an exception here.
            """
            raise NoMoreItems("No more items.")

        if not self.next_started:
            self.next_started = True

        page_response = await self._shared.requests.get(
            url=self.url,
            params={
                "cursor": self.next_cursor,
                "limit": self.page_size,
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


class PageNumberIterator(RobloxIterator):
    """
    Represents an iterator that is advanced with page numbers and sizes, like those seen on chat.roblox.com.

    Attributes:
        url: The endpoint to hit for new page data.
        page_number: The current page number.
        page_size: The size of each page.
        extra_parameters: Extra parameters to pass to the endpoint.
        handler: A callable object to use to convert raw endpoint data to parsed objects.
        handler_kwargs: Extra keyword arguments to pass to the handler.
    """

    def __init__(
            self,
            shared: ClientSharedObject,
            url: str,
            page_size: int = 10,
            extra_parameters: Optional[dict] = None,
            handler: Optional[Callable] = None,
            handler_kwargs: Optional[dict] = None
    ):
        super().__init__()

        self._shared: ClientSharedObject = shared

        self.url: str = url
        self.page_number: int = 1
        self.page_size: int = page_size

        self.extra_parameters: dict = extra_parameters or {}
        self.handler: Callable = handler
        self.handler_kwargs: dict = handler_kwargs or {}

        self.iterator_position = 0
        self.iterator_items = []

    async def next(self):
        """
        Advances the iterator to the next page.
        """
        page_response = await self._shared.requests.get(
            url=self.url,
            params={
                "pageNumber": self.page_number,
                "pageSize": self.page_size,
                **self.extra_parameters
            }
        )
        data = page_response.json()

        if len(data) == 0:
            raise NoMoreItems("No more items.")

        self.page_number += 1

        if self.handler:
            data = [
                self.handler(
                    shared=self._shared,
                    data=item_data,
                    **self.handler_kwargs
                ) for item_data in data
            ]

        return data
