import asyncio
from roblox.utilities.errors import c_errors
from httpx import AsyncClient, Response
from json.decoder import JSONDecodeError


class CleanAsyncClient(AsyncClient):
    """
    This is a clean-on-delete alternative to httpx.AsyncClient.
    """

    def __init__(self):
        super(CleanAsyncClient, self).__init__()

    def __del__(self):
        # asyncio.create_task(self.client.aclose())
        try:
            asyncio.get_event_loop().create_task(self.aclose())
        except RuntimeError:
            pass


# TODO is this good enough or did you want it an other way
def status_code_error(status_code):
    return c_errors[status_code]


class Requests:
    def __init__(self, security_cookie: str = None):
        self.session: CleanAsyncClient = CleanAsyncClient()
        """Session to use for requests."""
        self.xcsrf_token_name: str = "X-CSRF-TOKEN"
        """Header that will contain the X-CSRF-TOKEN. Should be set to "X-CSRF-TOKEN" under most circumstances."""

        self.session.headers["User-Agent"] = "Roblox/WinInet"
        self.session.headers["Referer"] = "www.roblox.com"

        if security_cookie:
            self.session.cookies[".ROBLOSECURITY"] = security_cookie

        self.status_code = int

    async def request(self, method, *args, **kwargs) -> Response:
        skip_roblox = kwargs.pop("skip_roblox", False)
        handle_xcsrf_token = kwargs.pop("handle_xcsrf_token", True)
        this_request = await self.session.request(method, *args, **kwargs)

        method = method.lower()

        if handle_xcsrf_token and (
                (method == "post") or (method == "put") or (method == "patch") or (method == "delete")):
            if self.xcsrf_token_name in this_request.headers:
                self.session.headers[self.xcsrf_token_name] = this_request.headers[self.xcsrf_token_name]
                if this_request.status_code == 403:  # Request failed, send it again
                    this_request = await self.session.request(method, *args, **kwargs)

        if kwargs.pop("stream", False):
            # Skip request checking and just get on with it.
            return this_request

        try:
            this_request_json = this_request.json()
        except JSONDecodeError:
            return this_request

        if isinstance(this_request_json, dict):
            try:
                get_request_error = this_request_json["errors"]
            except KeyError:
                return this_request
        else:
            return this_request

        if skip_roblox:
            return this_request

        request_exception = status_code_error(this_request.status_code)
        raise request_exception(f"[{this_request.status_code}] {get_request_error[0]['message']}")

    async def get(self, *args, **kwargs) -> Response:
        """
        Shortcut to self.request using the GET method.
        """

        return await self.request("GET", *args, **kwargs)

    async def post(self, *args, **kwargs) -> Response:
        """
        Shortcut to self.request using the POST method.
        """

        return await self.request("post", *args, **kwargs)

    async def patch(self, *args, **kwargs) -> Response:
        """
        Shortcut to self.request using the PATCH method.
        """

        return await self.request("patch", *args, **kwargs)

    async def delete(self, *args, **kwargs) -> Response:
        """
        Shortcut to self.request using the DELETE method.
        """

        return await self.request("delete", *args, **kwargs)

    def post_default(self, *args, **kwargs) -> Response:
        """
        This is just the default requests.post that handles Roblox-specific data.
        """

        kwargs["cookies"] = kwargs.pop("cookies", self.session.cookies)
        kwargs["headers"] = kwargs.pop("headers", self.session.headers)

        post_request = requests.post(*args, **kwargs)

        if self.xcsrf_token_name in post_request.headers:
            self.session.headers[self.xcsrf_token_name] = post_request.headers[self.xcsrf_token_name]
            post_request = requests.post(*args, **kwargs)

        self.session.cookies = post_request.cookies
        return post_request
