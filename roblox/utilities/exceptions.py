from httpx import HTTPStatusError as _HTTPStatusError, Request, Response


class HTTPStatusError(_HTTPStatusError):
    def __init__(self, message: str, *, request: Request, response: Response, errors: list = []):
        super(HTTPStatusError, self).__init__(message, request=request, response=response)
        self.errors = errors


class InvalidUserError(HTTPStatusError):
    pass
