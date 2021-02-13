from ro_py.utilities.errors import ApiError, c_errors
from json.decoder import JSONDecodeError
import requests
import httpx


class AsyncSession(httpx.AsyncClient):
    """
    This serves no purpose other than to get around an annoying HTTPX warning.
    """
    def __init__(self):
        super().__init__()

    def __del__(self):
        pass


def status_code_error(status_code):
    """
    Converts a status code to the proper exception.
    """
    if str(status_code) in c_errors:
        return c_errors[str(status_code)]
    else:
        return ApiError


class Requests:
    """
    This wrapper functions similarly to requests_async.Session, but made specifically for Roblox.
    """
    def __init__(self):
        self.session = AsyncSession()
        """Session to use for requests."""

        """
        Thank you @nsg for letting me know about this!
        This allows us to access some extra content.
        ▼▼▼
        """
        self.session.headers["User-Agent"] = "Roblox/WinInet"
        self.session.headers["Referer"] = "www.roblox.com"  # Possibly useful for some things

    async def request(self, method, *args, **kwargs):
        quickreturn = kwargs.pop("quickreturn", False)
        doxcsrf = kwargs.pop("doxcsrf", True)
        this_request = await self.session.request(method, *args, **kwargs)

        method = method.lower()

        if doxcsrf and ((method == "post") or (method == "put") or (method == "patch") or (method == "delete")):
            if "X-CSRF-TOKEN" in this_request.headers:
                self.session.headers['X-CSRF-TOKEN'] = this_request.headers["X-CSRF-TOKEN"]
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

        if quickreturn:
            return this_request

        request_exception = status_code_error(this_request.status_code)
        raise request_exception(f"[{this_request.status_code}] {get_request_error[0]['message']}")

    async def get(self, *args, **kwargs):
        """
        Essentially identical to requests_async.Session.get.
        """

        return await self.request("GET", *args, **kwargs)

    async def post(self, *args, **kwargs):
        """
        Essentially identical to requests_async.Session.post.
        """

        return await self.request("post", *args, **kwargs)

    async def patch(self, *args, **kwargs):
        """
        Essentially identical to requests_async.Session.patch.
        """

        return await self.request("patch", *args, **kwargs)

    async def delete(self, *args, **kwargs):
        """
        Essentially identical to requests_async.Session.delete.
        """

        return await self.request("delete", *args, **kwargs)

    def back_post(self, *args, **kwargs):
        kwargs["cookies"] = kwargs.pop("cookies", self.session.cookies)
        kwargs["headers"] = kwargs.pop("headers", self.session.headers)

        post_request = requests.post(*args, **kwargs)

        if "X-CSRF-TOKEN" in post_request.headers:
            self.session.headers['X-CSRF-TOKEN'] = post_request.headers["X-CSRF-TOKEN"]
            post_request = requests.post(*args, **kwargs)

        self.session.cookies = post_request.cookies
        return post_request
