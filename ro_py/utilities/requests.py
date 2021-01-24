from ro_py.utilities.errors import ApiError, c_errors
from ro_py.captcha import CaptchaMetadata
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

    async def get(self, *args, **kwargs):
        """
        Essentially identical to requests_async.Session.get.
        """

        quickreturn = kwargs.pop("quickreturn", False)

        get_request = await self.session.get(*args, **kwargs)

        if kwargs.pop("stream", False):
            # Skip request checking and just get on with it.
            return get_request

        try:
            get_request_json = get_request.json()
        except JSONDecodeError:
            return get_request

        if isinstance(get_request_json, dict):
            try:
                get_request_error = get_request_json["errors"]
            except KeyError:
                return get_request
        else:
            return get_request

        if quickreturn:
            return get_request

        raise status_code_error(get_request.status_code)(f"[{get_request.status_code}] {get_request_error[0]['message']}")

    def back_post(self, *args, **kwargs):
        kwargs["cookies"] = kwargs.pop("cookies", self.session.cookies)
        kwargs["headers"] = kwargs.pop("headers", self.session.headers)

        post_request = requests.post(*args, **kwargs)

        if "X-CSRF-TOKEN" in post_request.headers:
            self.session.headers['X-CSRF-TOKEN'] = post_request.headers["X-CSRF-TOKEN"]
            post_request = requests.post(*args, **kwargs)

        self.session.cookies = post_request.cookies
        return post_request

    async def post(self, *args, **kwargs):
        """
        Essentially identical to requests_async.Session.post.
        """

        quickreturn = kwargs.pop("quickreturn", False)
        doxcsrf = kwargs.pop("doxcsrf", True)

        post_request = await self.session.post(*args, **kwargs)

        if doxcsrf:
            if post_request.status_code == 403:
                if "X-CSRF-TOKEN" in post_request.headers:
                    self.session.headers['X-CSRF-TOKEN'] = post_request.headers["X-CSRF-TOKEN"]
                    post_request = await self.session.post(*args, **kwargs)

        try:
            post_request_json = post_request.json()
        except JSONDecodeError:
            return post_request

        if isinstance(post_request_json, dict):
            try:
                post_request_error = post_request_json["errors"]
            except KeyError:
                return post_request
        else:
            return post_request

        if quickreturn:
            return post_request

        raise status_code_error(post_request.status_code)(f"[{post_request.status_code}] {post_request_error[0]['message']}")

    async def patch(self, *args, **kwargs):
        """
        Essentially identical to requests_async.Session.patch.
        """

        patch_request = await self.session.patch(*args, **kwargs)

        if patch_request.status_code == 403:
            if "X-CSRF-TOKEN" in patch_request.headers:
                self.session.headers['X-CSRF-TOKEN'] = patch_request.headers["X-CSRF-TOKEN"]
                patch_request = await self.session.patch(*args, **kwargs)

        patch_request_json = patch_request.json()

        if isinstance(patch_request_json, dict):
            try:
                patch_request_error = patch_request_json["errors"]
            except KeyError:
                return patch_request
        else:
            return patch_request

        raise status_code_error(patch_request.status_code)(f"[{patch_request.status_code}] {patch_request_error[0]['message']}")

    async def delete(self, *args, **kwargs):
        """
        Essentially identical to requests_async.Session.delete.
        """

        delete_request = await self.session.delete(*args, **kwargs)

        if delete_request.status_code == 403:
            if "X-CSRF-TOKEN" in delete_request.headers:
                self.session.headers['X-CSRF-TOKEN'] = delete_request.headers["X-CSRF-TOKEN"]
                delete_request = await self.session.delete(*args, **kwargs)

        delete_request_json = delete_request.json()

        if isinstance(delete_request_json, dict):
            try:
                delete_request_error = delete_request_json["errors"]
            except KeyError:
                return delete_request
        else:
            return delete_request

        raise status_code_error(delete_request.status_code)(f"[{delete_request.status_code}] {delete_request_error[0]['message']}")

    async def get_captcha_metadata(self):
        captcha_meta_req = await self.get(
            url="https://apis.roblox.com/captcha/v1/metadata"
        )
        captcha_meta_raw = captcha_meta_req.json()
        return CaptchaMetadata(captcha_meta_raw)
