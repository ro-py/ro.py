from ro_py.utilities.errors import InvalidPageError
import enum


class SortOrder(enum.Enum):
    Ascending = "Asc"
    Descending = "Desc"


class PagedObject:
    def __init__(self, requests, url, extra_parameters=None, sort_order=SortOrder.Ascending, limit=10):
        if extra_parameters is None:
            extra_parameters = {}

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
        return page_req.json()

    def previous(self):
        if self.data["previousPageCursor"]:
            self.data = self._get_page(self.data["previousPageCursor"])
        else:
            raise InvalidPageError

    def next(self):
        if self.data["nextPageCursor"]:
            self.data = self._get_page(self.data["nextPageCursor"])
        else:
            raise InvalidPageError
