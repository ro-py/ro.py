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


class InvalidPageError(Exception):
    """Called when an Page is invalid"""
    pass


c_errors = {
    400: BadRequest,
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
    409: Conflict,
    429: TooManyRequests,
    500: InternalServerError,
    502: BadGateway
}
