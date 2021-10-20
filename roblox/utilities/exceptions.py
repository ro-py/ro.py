"""

Contains exceptions used by ro.py.

"""

from typing import Optional
from httpx import Response


class RobloxException(Exception):
    """
    Base exception for all of ro.py.
    """
    pass


def _generate_error_string(errors: list):
    parsed_errors = []
    for error in errors:
        # Make each error into a parsed string
        error_code = error["code"]
        error_message = error.get("message")

        parsed_error = f"\t{error_code}: {error_message}"

        error_messages = []

        error_user_facing_message = error.get("userFacingMessage")
        error_field = error.get("field")
        error_retryable = error.get("retryable")

        if error_user_facing_message:
            # Add the parenthesis-wrapped user facing message
            error_messages.append(f"User-facing message: {error_user_facing_message}")

        if error_field:
            # Add the field, which is the name of the key in the request body that caused the error
            error_messages.append(f"Field: {error_field}")

        if error_retryable is not None:
            error_messages.append(f"Retryable: {error_retryable}")

        if error_messages:
            error_message_string = "\n\t\t".join(error_messages)
            parsed_error += f"\n\t\t{error_message_string}"

        parsed_errors.append(parsed_error)

    # Turn the parsed errors into a joined string
    return "\n".join(parsed_errors)


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
        if errors:
            error_string = _generate_error_string(errors)
            super().__init__(f"""{response.status_code} {response.reason_phrase}: {response.url}.\n\nErrors:
{error_string}""")
        else:
            super().__init__(f"""{response.status_code} {response.reason_phrase}: {response.url}""")


class InvalidRole(RobloxException):
    """
    Raised when a role doesn't exist.
    """
    pass
