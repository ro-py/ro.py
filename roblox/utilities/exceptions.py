from httpx import HTTPStatusError as _HTTPStatusError, Request, Response


class HTTPStatusError(_HTTPStatusError):
    def __init__(self, message: str, *, request: Request, response: Response, errors=None):
        super(HTTPStatusError, self).__init__(message, request=request, response=response)
        if errors is None:
            errors = []
        self.errors = errors
