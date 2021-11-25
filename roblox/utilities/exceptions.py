"""

Contains exceptions used by ro.py.

"""

from typing import Optional, List, Dict, Type

from httpx import Response


# Generic exceptions

class RobloxException(Exception):
    """
    Base exception for all of ro.py.
    """
    pass


# Other objects

class ResponseError:
    """
    Represents an error returned by a Roblox game server.

    Attributes:
        code: The error code.
        message: The error message.
        user_facing_message: A more simple error message intended for frontend use.
        field: The field causing this error.
        retryable: Whether retrying this exception could supress this issue.
    """

    def __init__(self, data: dict):
        self.code: int = data["code"]
        self.message: Optional[str] = data.get("message")
        self.user_facing_message: Optional[str] = data.get("userFacingMessage")
        self.field: Optional[str] = data.get("field")
        self.retryable: Optional[str] = data.get("retryable")


# HTTP exceptions
# Exceptions that Roblox endpoints do not respond with are not included here.

class HTTPException(RobloxException):
    """
    Exception that's raised when an HTTP request fails.

    Attributes:
        response: The HTTP response object.
        status: The HTTP response status code.
        errors: A list of Roblox response errors.
    """

    def __init__(self, response: Response, errors: Optional[list] = None):
        """
        Arguments:
            response: The raw response object.
            errors: A list of errors.
        """
        self.response: Response = response
        self.status: int = response.status_code
        self.errors: List[ResponseError]

        if errors:
            self.errors = [
                ResponseError(data=error_data) for error_data in errors
            ]
        else:
            self.errors = []

        if self.errors:
            error_string = self._generate_string()
            super().__init__(
                f"{response.status_code} {response.reason_phrase}: {response.url}.\n\nErrors:\n{error_string}")
        else:
            super().__init__(f"{response.status_code} {response.reason_phrase}: {response.url}")

    def _generate_string(self) -> str:
        parsed_errors = []
        for error in self.errors:
            # Make each error into a parsed string
            parsed_error = f"\t{error.code}: {error.message}"
            error_messages = []

            error.user_facing_message and error_messages.append(f"User-facing message: {error.user_facing_message}")
            error.field and error_messages.append(f"Field: {error.field}")
            error.retryable and error_messages.append(f"Retryable: {error.retryable}")

            if error_messages:
                error_message_string = "\n\t\t".join(error_messages)
                parsed_error += f"\n\t\t{error_message_string}"

            parsed_errors.append(parsed_error)

        # Turn the parsed errors into a joined string
        return "\n".join(parsed_errors)


class BadRequest(HTTPException):
    """HTTP exception raised for status code 400."""
    pass


class Unauthorized(HTTPException):
    """HTTP exception raised for status code 401. This usually means you aren't properly authenticated."""


class Forbidden(HTTPException):
    """HTTP exception raised for status code 403. This usually means the X-CSRF-Token was not properly provided."""
    pass


class NotFound(HTTPException):
    """
    HTTP exception raised for status code 404.
    This usually means we have an internal URL issue - please make a GitHub issue about this!
    """
    pass


class TooManyRequests(HTTPException):
    """
    HTTP exception raised for status code 429.
    This means that Roblox has [ratelimited](https://en.wikipedia.org/wiki/Rate_limiting) you.
    """
    pass


class InternalServerError(HTTPException):
    """
    HTTP exception raised for status code 500.
    This usually means that there was an issue on Roblox's end, but due to faulty coding on Roblox's part this can
    sometimes mean that an endpoint used internally was disabled or that invalid parameters were passed.
    """
    pass


_codes_exceptions: Dict[int, Type[HTTPException]] = {
    400: BadRequest,
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
    429: TooManyRequests,
    500: InternalServerError
}


def get_exception_from_status_code(code: int) -> Type[HTTPException]:
    """
    Gets an exception that should be raised instead of the generic HTTPException for this status code.
    """
    return _codes_exceptions.get(code) or HTTPException


# Misc exceptions
class InvalidRole(RobloxException):
    """
    Raised when a role doesn't exist.
    """
    pass


class NoMoreItems(RobloxException):
    """
    Raised when there are no more items left to iterate through.
    """
    pass


# Exceptions raised for certain Client methods
class ItemNotFound(RobloxException):
    """
    Raised for invalid items.
    """

    def __init__(self, message: str, response: Optional[Response] = None):
        """
        Arguments:
            response: The raw response object.
        """
        self.response: Optional[Response] = response
        self.status: Optional[int] = response.status_code if response else None
        super().__init__(message)


class AssetNotFound(ItemNotFound):
    """
    Raised for invalid asset IDs.
    """
    pass


class BadgeNotFound(ItemNotFound):
    """
    Raised for invalid badge IDs.
    """
    pass


class GroupNotFound(ItemNotFound):
    """
    Raised for invalid badge IDs.
    """
    pass


class PlaceNotFound(ItemNotFound):
    """
    Raised for invalid place IDs.
    """
    pass


class PluginNotFound(ItemNotFound):
    """
    Raised for invalid plugin IDs.
    """
    pass


class UniverseNotFound(ItemNotFound):
    """
    Raised for invalid universe IDs.
    """
    pass


class UserNotFound(ItemNotFound):
    """
    Raised for invalid user IDs or usernames.
    """
    pass
