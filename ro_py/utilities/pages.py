import enum


class SortOrder(enum.Enum):
    Ascending = "Asc"
    Descending = "Desc"


class PagedObject:
    def __init__(self, requests, url, sort_order=SortOrder.Ascending, limit=10):
        self.requests = requests
        self.url = url
        self.page = 0

    def _get_page(self):
        
