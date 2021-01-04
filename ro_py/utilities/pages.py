from ro_py.utilities.errors import InvalidPageError
import enum


class SortOrder(enum.Enum):
    """
    Order in which page data should load in.
    """
    Ascending = "Asc"
    Descending = "Desc"


class Page:
    """
    Represents a single page from a Pages object.
    """
    def __init__(self, requests, data, handler=None, handler_args=None):
        self.previous_page_cursor = data["previousPageCursor"]
        """Cursor to navigate to the previous page."""
        self.next_page_cursor = data["nextPageCursor"]
        """Cursor to navigate to the next page."""

        self.data = data["data"]
        """Raw data from this page."""

        if handler:
            self.data = handler(requests, self.data, handler_args)


class Pages:
    """
    Represents a paged object.

    !!! warning
        This object is *slow*, especially with a custom handler.
        Automatic page caching will be added in the future. It is suggested to
        cache the pages yourself if speed is required.
    """
    def __init__(self, requests, url, sort_order=SortOrder.Ascending, limit=10, extra_parameters=None, handler=None, handler_args=None):
        if extra_parameters is None:
            extra_parameters = {}

        self.handler = handler
        """Function that is passed to Page as data handler."""

        extra_parameters["sortOrder"] = sort_order.value
        extra_parameters["limit"] = limit

        self.parameters = extra_parameters
        """Extra parameters for the request."""
        self.requests = requests
        """Requests object."""
        self.url = url
        """URL containing the paginated data, accessible with a GET request."""
        self.page = 0
        """Current page number."""

        self.data = self._get_page()

    async def _get_page(self, cursor=None):
        """
        Gets a page at the specified cursor position.
        """
        this_parameters = self.parameters
        if cursor:
            this_parameters["cursor"] = cursor

        page_req = await self.requests.get(
            url=self.url,
            params=this_parameters
        )
        return Page(
            requests=self.requests,
            data=page_req.json(),
            handler=self.handler,
            handler_args=handler_args
        )

    async def previous(self):
        """
        Moves to the previous page.
        """
        if self.data.previous_page_cursor:
            self.data = await self._get_page(self.data.previous_page_cursor)
        else:
            raise InvalidPageError

    async def next(self):
        """
        Moves to the next page.
        """
        if self.data.next_page_cursor:
            self.data = await self._get_page(self.data.next_page_cursor)
        else:
            raise InvalidPageError
