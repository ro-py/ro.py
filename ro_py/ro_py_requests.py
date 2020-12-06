"""

ro.py > ro_py_requests.py

This file houses functions and classes that pertain to web requests.
It is essentially a very limited Roblox-specific version of requests.

"""

from ro_py.errors import ApiError
import requests


def get(*args, **kwargs):
    get_request = requests.get(*args, **kwargs)

    try:
        get_request_error = get_request.json()["errors"]
    except KeyError:
        return get_request

    raise ApiError(f"[{str(get_request.status_code)}] {get_request_error[0]['message']}")


def post(*args, **kwargs):
    post_request = requests.post(*args, **kwargs)
    try:
        post_request_error = post_request.json()["errors"]
    except KeyError:
        return post_request

    raise ApiError(post_request_error[0]["message"])

