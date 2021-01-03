"""

This file houses functions and classes that pertain to the Roblox API documentation pages.
I don't know if this is really that useful, but it might be useful for an API browser program, or for accessing
endpoints that aren't supported directly by ro.py yet.

"""

from lxml import html
from io import StringIO


class EndpointDocs:
    def __init__(self, requests, docs_url):
        self.requests = requests
        self.url = docs_url

    async def get_versions(self):
        docs_req = self.requests.get(self.url + "/docs")
