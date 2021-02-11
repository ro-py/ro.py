"""

ro.py > errors.py

This file houses custom exceptions unique to this module.

"""


# The following are HTTP generic errors used by utilities/requests.py
class ApiError(Exception):
    """Called in requests when an API request fails with an error code that doesn't have an independent error."""
    pass


class BadRequest(ApiError):
    """400 HTTP error"""
    pass


class Unauthorized(ApiError):
    """401 HTTP error"""
    pass


class Forbidden(ApiError):
    """403 HTTP error"""
    pass


class NotFound(ApiError):
    """404 HTTP error (also used for other things)"""
    pass


class Conflict(ApiError):
    """409 HTTP error"""
    pass


class TooManyRequests(ApiError):
    """429 HTTP error"""
    pass


class InternalServerError(ApiError):
    """500 HTTP error"""
    pass


class BadGateway(ApiError):
    """502 HTTP error"""
    pass


# The following errors are specific to certain parts of ro.py
class NotLimitedError(Exception):
    """Called when code attempts to read limited-only information."""
    pass


class InvalidIconSizeError(Exception):
    """Called when code attempts to pass in an improper size to a thumbnail function."""
    pass


class InvalidShotTypeError(Exception):
    """Called when code attempts to pass in an improper avatar image type to a thumbnail function."""
    pass


class ChatError(Exception):
    """Called in chat when a chat action fails."""


class InvalidPageError(Exception):
    """Called when an invalid page is requested."""


class UserDoesNotExistError(Exception):
    """Called when a user does not exist."""


class GameJoinError(Exception):
    """Called when an error occurs when joining a game."""


class InvalidPlaceIDError(Exception):
    """Called when place ID is invalid."""


class IncorrectKeyError(Exception):
    """Raised when the api key for 2captcha is incorrect."""
    pass


class InsufficientCreditError(Exception):
    """Raised when there is insufficient credit in 2captcha."""
    pass


class NoAvailableWorkersError(Exception):
    """Raised when there are no available workers."""
    pass


c_errors = {
    "400": BadRequest,
    "401": Unauthorized,
    "403": Forbidden,
    "404": NotFound,
    "409": Conflict,
    "429": TooManyRequests,
    "500": InternalServerError,
    "502": BadGateway
}
