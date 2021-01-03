"""

This file houses functions and classes that pertain to the Roblox API documentation pages.
I don't know if this is really that useful, but it might be useful for an API browser program, or for accessing
endpoints that aren't supported directly by ro.py yet.

"""

from lxml import html
from io import StringIO


class EndpointDocsPathRequestTypeParameters:
    def __init__(self):
        pass


class EndpointDocsPathRequestType:
    def __init__(self, data):
        self.tags = data["tags"]
        self.summary = data["summary"]
        self.description = data["description"]
        self.consumes = data["consumes"]
        self.produces = data["produces"]


class EndpointDocsPath:
    def __init__(self, data):
        self.data = data
        for type_k, type_v in self.data:
            setattr(self, type_k, EndpointDocsPathRequestType(type_v))


class EndpointDocsDataInfo:
    def __init__(self, data):
        self.version = data["version"]
        self.title = data["title"]


class EndpointDocsData:
    def __init__(self, data):
        self.swagger_version = data["swagger"]
        self.info = EndpointDocsDataInfo(data["info"])
        self.host = data["host"]
        self.schemes = data["schemes"]
        self.paths = {}
        for path_k, path_v in data["paths"].items():
            self.paths[path_k] = EndpointDocsPath(path_v)


class EndpointDocs:
    def __init__(self, requests, docs_url):
        self.requests = requests
        self.url = docs_url

    async def get_versions(self):
        docs_req = self.requests.get(self.url + "/docs")
        root = html.parse(StringIO(docs_req.text)).getroot()
        try:
            vs_element = root.get_element_by_id("version-selector")
            return vs_element.value_options
        except KeyError:
            return ["v1"]

    async def get_data_for_version(self, version):
        data_req = self.requests.get(self.url + "/docs/json/" + version)
        version_data = data_req.json()
        return EndpointDocsData(version_data)
