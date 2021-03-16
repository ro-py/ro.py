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

        def __init__(self, cso, data, pages, handler=None, handler_args=None):
            self.cso = cso
            """Client shared object."""
            self.previous_page_cursor = data["previousPageCursor"]
            """Cursor to navigate to the previous page."""
            self.next_page_cursor = data["nextPageCursor"]
            """Cursor to navigate to the next page."""
            self.data = data["data"]
            """Raw data from this page."""
            self.pages = pages
            """Pages object for iteration."""

            self.handler = handler
            self.handler_args = handler_args
            if handler:
                self.data = handler(self.cso, self.data, handler_args)

        def update(self, data):
            self.previous_page_cursor = data["previousPageCursor"]
            self.next_page_cursor = data["nextPageCursor"]
            self.data = data["data"]
            if self.handler:
                self.data = self.handler(self.cso, data["data"], self.handler_args)

        def __getitem__(self, key):
            return self.data[key]


class Pages:
    """
    Represents a paged object.

    !!! warning
        This object is *slow*, especially with a custom handler.
        Automatic page caching will be added in the future. It is suggested to
        cache the pages yourself if speed is required.
    """
    def __init__(self, cso, url, sort_order=SortOrder.Ascending, limit=10, extra_parameters=None, handler=None, handler_args=None):
        if extra_parameters is None:
            extra_parameters = {}

        self.handler = handler
        """Function that is passed to Page as data handler."""

        extra_parameters["sortOrder"] = sort_order.value
        extra_parameters["limit"] = limit

        self.parameters = extra_parameters
        """Extra parameters for the request."""
        self.cso = cso
        self.requests = cso.requests
        """Requests object."""
        self.url = url
        """URL containing the paginated data, accessible with a GET request."""
        self.page = 0
        """Current page number."""
        self.handler_args = handler_args
        self.data = None
        self.i = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.i == len(self.data.data):
            if not self.data.next_page_cursor:
                self.i = 0
                raise StopAsyncIteration
            await self.next()
            self.i = 0
        data = self.data.data[self.i]
        self.i += 1
        return data

    async def get_page(self, cursor=None):
        """
        Gets a page at the specified cursor position.
        """
        this_parameters = self.parameters
        if cursor:
            this_parameters["cursor"] = cursor

        for name, value in self.parameters.items():
            this_parameters[name] = value

        page_req = await self.requests.get(
            url=self.url,
            params=this_parameters
        )
        if self.data:
            self.data.update(page_req.json())
            return
        self.data = Page(
            cso=self.cso,
            data=page_req.json(),
            pages=self,
            handler=self.handler,
            handler_args=self.handler_args
        )

    async def previous(self):
        """
        Moves to the previous page.
        """
        if self.data.previous_page_cursor:
            await self.get_page(self.data.previous_page_cursor)
        else:
            raise InvalidPageError

    async def next(self):
        """
        Moves to the next page.
        """
        if self.data.next_page_cursor:
            await self.get_page(self.data.next_page_cursor)
        else:
            raise InvalidPageError
