from httpx import HTTPStatusError as _HTTPStatusError, Request, Response


class HTTPStatusError(_HTTPStatusError):
    """
    Attributes:
        errors: The error codes
    """

    def __init__(self, message: str, *, request: Request, response: Response, errors=None):
        """
        Arguments:
            message: Error message
            request: Request send
            response: response reserved
            errors: errors
            *: Unknown
        """
        super(HTTPStatusError, self).__init__(message, request=request, response=response)
        if errors is None:
            errors = []
        self.errors = errors


class InvalidRole(Exception):
    """
    Raised when a role doesn't exist.
    """
    pass
