import asyncio
from httpx import AsyncClient, Response
from json import JSONDecodeError
from .exceptions import HTTPStatusError


class CleanAsyncClient(AsyncClient):
    """
    This is a clean-on-delete version of httpx.AsyncClient.
    """

    def __init__(self):
        super().__init__()

    def __del__(self):
        try:
            asyncio.get_event_loop().create_task(self.aclose())
        except RuntimeError:
            pass


def status_code_error(status_code):
    pass


class Requests:
    """
    A special request object that implements special functionality required to connect to some Roblox endpoints.
    """
    def __init__(self):
        self.session: CleanAsyncClient = CleanAsyncClient()
        """
        Base session object to use when sending requests.
        By default, this is an instance of CleanAsyncClient.
        """

        self.xcsrf_token_name: str = "X-CSRF-Token"
        """
        The header that will contain the Cross-Site Request Forgery token.
        Should be set to `X-CSRF-Token` under most circumstances.
        """

        self.xcsrf_allowed_methods: dict[str, bool] = {
            "post": True,
            "put": True,
            "patch": True,
            "delete": True
        }
        """
        A dictionary where the keys are HTTP method types and values are whether the X-CSRF-Token should be handled for
        that method. Keys must be in lowercase.
        """

        self.session.headers["User-Agent"] = "Roblox/WinInet"
        self.session.headers["Referer"] = "www.roblox.com"

    async def request(self, method: str, *args, **kwargs) -> Response:
        skip_roblox = kwargs.pop("skip_roblox", False)
        handle_xcsrf_token = kwargs.pop("handle_xcsrf_token", True)
        skip_roblox = kwargs.pop("skip_roblox", False)

        response = await self.session.request(method, *args, **kwargs)

        if skip_roblox:
            return response

        method = method.lower()

        if handle_xcsrf_token and self.xcsrf_token_name in response.headers and self.xcsrf_allowed_methods.get(method):
            self.session.headers[self.xcsrf_token_name] = response.headers[self.xcsrf_token_name]
            if response.status_code == 403:  # Request failed, send it again
                response = await self.session.request(method, *args, **kwargs)

        if kwargs.get("stream"):
            # Streamed responses should not be decoded, so we immediately return the response.
            return response

        if response.is_error:
            # Something went wrong, parse an error
            content_type = response.headers.get("Content-Type")
            errors = None
            if content_type and content_type.startswith("application/json"):
                data = None
                try:
                    data = response.json()
                except JSONDecodeError:
                    pass
                errors = data and data.get("errors")
            if errors:
                parsed_errors = []
                for error in errors:
                    # Make each error into a parsed string
                    error_code = error["code"]
                    error_message = error.get("message")

                    parsed_error = f"{error_code}: {error_message}"

                    error_messages = []

                    error_user_facing_message = error.get("userFacingMessage")
                    error_field = error.get("field")
                    error_retryable = error.get("retryable")

                    if error_user_facing_message:
                        # Add the parenthesis-wrapped user facing message
                        error_messages.append(f"User-facing message: {error_user_facing_message})")

                    if error_field:
                        # Add the field, which is the name of the key in the request body that caused the error
                        error_messages.append(f"Field: {error_field}")

                    if error_retryable is not None:
                        error_messages.append(f"Retryable: {error_retryable}")

                    if error_messages:
                        error_message_string = ", ".join(error_messages)
                        parsed_error += f" ({error_message_string})"

                    parsed_errors.append(parsed_error)

                # Turn the parsed errors into a joined string
                parsed_error_string = "\n".join(parsed_errors)

                exception = HTTPStatusError(
                    message=f"""{response.status_code} {response.reason_phrase}: {response.url}. Errors:
{parsed_error_string}""",
                    request=response.request,
                    response=response,
                    errors=errors
                )
            else:
                exception = HTTPStatusError(
                    message=f"{response.status_code} {response.reason_phrase}: {response.url}",
                    request=response.request,
                    response=response
                )
            raise exception
        else:
            return response

    def get(self, *args, **kwargs):
        """
        Shortcut to self.request using the GET method.
        """

        return self.request("GET", *args, **kwargs)

    def post(self, *args, **kwargs):
        """
        Shortcut to self.request using the POST method.
        """

        return self.request("post", *args, **kwargs)

    def patch(self, *args, **kwargs):
        """
        Shortcut to self.request using the PATCH method.
        """

        return self.request("patch", *args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Shortcut to self.request using the DELETE method.
        """

        return self.request("delete", *args, **kwargs)
