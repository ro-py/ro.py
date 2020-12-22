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

    def _get_page(self, cursor=None):
        this_parameters = self.parameters
        if cursor:
            this_parameters["cursor"] = cursor
        
        self.requests.get(
            url=self.url,
            params=this_parameters
        )
