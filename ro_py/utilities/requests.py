from ro_py.utilities.errors import ApiError
from json.decoder import JSONDecodeError
from cachecontrol import CacheControl
import requests_async


class Requests:
    def __init__(self, cache=True, jmk_endpoint="https://roblox.jmksite.dev/"):
        self.session = requests_async.Session()
        if cache:
            self.session = CacheControl(self.session)
        """
        Thank you @nsg for letting me know about this!
        This allows us to access some extra content.
        ▼▼▼
        """
        self.session.headers["User-Agent"] = "Roblox/WinInet"

    async def get(self, *args, **kwargs):
        """
        Essentially identical to requests.Session.get.
        """

        get_request = self.session.get(*args, **kwargs)

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

        raise ApiError(f"[{str(get_request.status_code)}] {get_request_error[0]['message']}")

    async def post(self, *args, **kwargs):
        """
        Essentially identical to requests.Session.post.
        """

        post_request = self.session.post(*args, **kwargs)

        if post_request.status_code == 403:
            if "X-CSRF-TOKEN" in post_request.headers:
                self.session.headers['X-CSRF-TOKEN'] = post_request.headers["X-CSRF-TOKEN"]
                post_request = self.session.post(*args, **kwargs)

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

        raise ApiError(f"[{str(post_request.status_code)}] {post_request_error[0]['message']}")

    async def patch(self, *args, **kwargs):
        """
        Essentially identical to requests.Session.patch.
        """

        patch_request = self.session.patch(*args, **kwargs)

        if patch_request.status_code == 403:
            if "X-CSRF-TOKEN" in patch_request.headers:
                self.session.headers['X-CSRF-TOKEN'] = patch_request.headers["X-CSRF-TOKEN"]
                patch_request = self.session.patch(*args, **kwargs)

        patch_request_json = patch_request.json()

        if isinstance(patch_request_json, dict):
            try:
                patch_request_error = patch_request_json["errors"]
            except KeyError:
                return patch_request
        else:
            return patch_request

        raise ApiError(f"[{str(patch_request.status_code)}] {patch_request_error[0]['message']}")
