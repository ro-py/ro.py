"""

This module contains classes used internally by ro.py for sending requests to Roblox endpoints.

"""

from __future__ import annotations

import asyncio
from datetime import datetime
from json import JSONDecodeError
from typing import Optional

from dateutil.parser import parse
from httpx import AsyncClient, Response

from .exceptions import HTTPStatusError
from ..utilities.url import URLGenerator


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


class Requests:
    """
    A special request object that implements special functionality required to connect to some Roblox endpoints.

    Attributes:
        session: Base session object to use when sending requests.
        xcsrf_token_name: The header that will contain the Cross-Site Request Forgery token
        xcsrf_allowed_methods: The methods allowed for
        that method. Keys must be in lowercase.
        parse_bans: Whether to parse ban data.
        url_generator: URL generator for ban parsing.
    """

    def __init__(
            self,
            url_generator: URLGenerator = None,
            session: CleanAsyncClient = None,
            xcsrf_token_name: str = "X-CSRF-Token",
            parse_bans: bool = True
    ):
        """
        Arguments:
            session: A custom session object to use for sending requests, compatible with httpx.AsyncClient.
            xcsrf_token_name: The header to place X-CSRF-Token data into.
            parse_bans: Whether to give extra information about a banned user.
            url_generator: URL generator for ban parsing.
        """
        self._url_generator: Optional[URLGenerator] = url_generator
        self.session: CleanAsyncClient

        if session is None:
            self.session = CleanAsyncClient()
        else:
            self.session = session

        self.xcsrf_token_name: str = xcsrf_token_name

        self.xcsrf_allowed_methods: dict[str, bool] = {
            "post": True,
            "put": True,
            "patch": True,
            "delete": True
        }

        self.parse_bans: bool = parse_bans

        self.session.headers["User-Agent"] = "Roblox/WinInet"
        self.session.headers["Referer"] = "www.roblox.com"

    async def request(self, method: str, *args, **kwargs) -> Response:
        """
        Arguments:
            method: method used for the request
            *args: Everything and noting.
            **kwargs: Everything and noting.

        Returns:
            Response
        """

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

                    if self.parse_bans and error_message == "User is moderated":
                        # This is a ban error message, send another request for data.
                        # This request needs to be safe and no errors can be raised here.
                        try:
                            ban_response = await self.session.get(
                                url=self._url_generator.get_url("usermoderation", "v1/not-approved")
                            )
                            ban_data = ban_response.json()

                            punished_user_id: int = ban_data["punishedUserId"]
                            message_to_user: str = ban_data["messageToUser"]
                            punishment_type_description: str = ban_data["punishmentTypeDescription"]
                            punishment_id: int = ban_data["punishmentId"]
                            begin_date: Optional[datetime] = None
                            end_date: Optional[datetime] = None

                            if ban_data["beginDate"]:
                                begin_date = parse(ban_data["beginDate"])

                            if ban_data["endDate"]:
                                end_date = parse(ban_data["endDate"])

                            error_messages.append(f"Punished User ID: {punished_user_id}")
                            error_messages.append(f"Punishment Type: {punishment_type_description}")
                            error_messages.append(f"Punishment ID: {punishment_id}")
                            error_messages.append(f"Ban Message: {message_to_user}")

                            if begin_date:
                                parsed_begin_date = begin_date.strftime("%m/%d/%Y, %H:%M:%S")
                                error_messages.append(f"Begin Date: {parsed_begin_date}")
                            else:
                                error_messages.append(f"Begin Date: None")

                            if end_date:
                                parsed_end_date = end_date.strftime("%m/%d/%Y, %H:%M:%S")
                                error_messages.append(f"End Date: {parsed_end_date}")
                            else:
                                error_messages.append(f"End Date: None")

                            not_approved_url = self._url_generator.get_url("www", "not-approved")
                            error_messages.append(f"For more information, please see {not_approved_url}.")
                            error_messages.append(
                                f"If you wish to appeal, please contact Roblox: https://www.roblox.com/support")

                        except Exception:
                            # don't throw errors
                            pass

                    if error_messages:
                        error_message_string = "\n\t\t".join(error_messages)
                        parsed_error += f"\n\t\t{error_message_string}"

                    parsed_errors.append(parsed_error)

                # Turn the parsed errors into a joined string
                parsed_error_string = "\n".join(parsed_errors)

                exception = HTTPStatusError(
                    message=f"""{response.status_code} {response.reason_phrase}: {response.url}.\n\nErrors:
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

        Arguments:
            *args: Everything and noting.
            **kwargs: Everything and noting.

        Returns:
            Response
        """

        return self.request("GET", *args, **kwargs)

    def post(self, *args, **kwargs):
        """
        Shortcut to self.request using the POST method.

        Arguments:
            *args: Everything and noting.
            **kwargs: Everything and noting.
        """

        return self.request("post", *args, **kwargs)

    def patch(self, *args, **kwargs):
        """
        Shortcut to self.request using the PATCH method.

        Arguments:
            *args: Everything and noting.
            **kwargs: Everything and noting.

        Returns:
            Response
        """

        return self.request("patch", *args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Shortcut to self.request using the DELETE method.

        Arguments:
            *args: Everything and noting.
            **kwargs: Everything and noting.

        Returns:
            Response
        """

        return self.request("delete", *args, **kwargs)
