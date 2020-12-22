from ro_py.utilities.errors import InvalidPageError
import enum


class SortOrder(enum.Enum):
    Ascending = "Asc"
    Descending = "Desc"


class Page:
    def __init__(self, requests, data, handler=None):
        self.previous_page_cursor = data["previousPageCursor"]
        self.next_page_cursor = data["nextPageCursor"]
        if handler:
            self.data = handler(requests, data["data"])
        else:
            self.data = data["data"]


class Pages:
    def __init__(self, requests, url, sort_order=SortOrder.Ascending, limit=10, extra_parameters=None, handler=None):
        if extra_parameters is None:
            extra_parameters = {}

        self.handler = handler

        extra_parameters["sortOrder"] = sort_order.value
        extra_parameters["limit"] = limit

        self.parameters = extra_parameters
        self.requests = requests
        self.url = url
        self.page = 0

        self.data = self._get_page()

    def _get_page(self, cursor=None):
        this_parameters = self.parameters
        if cursor:
            this_parameters["cursor"] = cursor

        page_req = self.requests.get(
            url=self.url,
            params=this_parameters
        )
        return Page(
            requests=self.requests,
            data=page_req.json(),
            handler=self.handler
        )

    def previous(self):
        if self.data.previous_page_cursor:
            self.data = self._get_page(self.data.previous_page_cursor)
        else:
            raise InvalidPageError

    def next(self):
        if self.data.next_page_cursor:
            self.data = self._get_page(self.data.next_page_cursor)
        else:
            raise InvalidPageError
