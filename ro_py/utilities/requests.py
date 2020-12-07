from ro_py.utilities.errors import ApiError
import requests


class Requests:
    def __init__(self):
        self.cookies = {}
        self.headers = {}

    def get(self, *args, **kwargs):
        kwargs["cookies"] = self.cookies
        kwargs["headers"] = self.headers

        get_request = requests.get(*args, **kwargs)
        try:
            get_request_error = get_request.json()["errors"]
        except KeyError:
            return get_request

        raise ApiError(f"[{str(get_request.status_code)}] {get_request_error[0]['message']}")

    def post(self, *args, **kwargs):
        kwargs["cookies"] = self.cookies
        kwargs["headers"] = self.headers

        post_request = requests.post(*args, **kwargs)
        if post_request.status_code == 403:
            if "X-CSRF-TOKEN" in post_request.headers:
                self.headers['X-CSRF-TOKEN'] = post_request.headers["X-CSRF-TOKEN"]
                post_request = requests.post(*args, **kwargs)

        try:
            post_request_error = post_request.json()["errors"]
        except KeyError:
            return post_request

        raise ApiError(f"[{str(post_request.status_code)}] {post_request_error[0]['message']}")

    def update_xsrf(self, url="https://www.roblox.com/favorite/toggle"):
        xsrf_req = requests.post(url)
        self.headers['X-CSRF-TOKEN'] = xsrf_req.headers["X-CSRF-TOKEN"]
