"""

Contains exceptions used by ro.py.

"""

from typing import Optional, List
from httpx import Response


class RobloxException(Exception):
    """
    Base exception for all of ro.py.
    """
    pass


class ResponseError:
    """
    Represents a single error in an "errors" list.
    """
    def __init__(self, data: dict):
        self.code: int = data["code"]
        self.message: Optional[str] = data.get("message")
        self.user_facing_message: Optional[str] = data.get("userFacingMessage")
        self.field: Optional[str] = data.get("field")
        self.retryable: Optional[str] = data.get("retryable")


class HTTPException(RobloxException):
    """
    Exception that's raised when an HTTP request fails.
    """
    def __init__(self, response: Response, errors: Optional[list] = None):
        """
        Arguments:
            response: The raw response object.
            errors: A list of errors.
        """
        self.response: Response = response
        self.status: int = response.status_code
        self.errors: List[ResponseError] = [
            ResponseError(data=error_data) for error_data in errors
        ]
        if errors:
            error_string = self._generate_string()
            super().__init__(f"""{response.status_code} {response.reason_phrase}: {response.url}.\n\nErrors:
{error_string}""")
        else:
            super().__init__(f"""{response.status_code} {response.reason_phrase}: {response.url}""")

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


class InvalidRole(RobloxException):
    """
    Raised when a role doesn't exist.
    """
    pass
