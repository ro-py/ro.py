"""

This module contains classes used internally by ro.py for sending requests to Roblox endpoints.

"""

from __future__ import annotations

import asyncio
from json import JSONDecodeError
from typing import Optional, Union, Any

from httpx import AsyncClient, Response, USE_CLIENT_DEFAULT
from httpx._client import UseClientDefault
from httpx._types import RequestData, RequestContent, URLTypes, RequestFiles, QueryParamTypes, HeaderTypes, \
    CookieTypes, AuthTypes, TimeoutTypes

from .exceptions import get_exception_from_status_code
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
        url_generator: URL generator for ban parsing.
    """

    def __init__(
            self,
            url_generator: URLGenerator = None,
            session: CleanAsyncClient = None,
            xcsrf_token_name: str = "X-CSRF-Token"
    ):
        """
        Arguments:
            session: A custom session object to use for sending requests, compatible with httpx.AsyncClient.
            xcsrf_token_name: The header to place X-CSRF-Token data into.
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

        self.session.headers["User-Agent"] = "Roblox/WinInet"
        self.session.headers["Referer"] = "www.roblox.com"

    async def request(
            self,
            method: str,
            url: URLTypes,
            *,
            content: RequestContent = None,
            data: RequestData = None,
            files: RequestFiles = None,
            json: Any = None,
            params: QueryParamTypes = None,
            headers: HeaderTypes = None,
            cookies: CookieTypes = None,
            auth: Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
            allow_redirects: Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
            timeout: Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
            handle_xcsrf_token: bool = True,
            skip_roblox: bool = False
    ) -> Response:
        """
        For documentation on these parameters, please see httpx's docs at https://www.python-httpx.org/
            and the Requests documentation at https://github.com/psf/requests/blob/main/requests/api.py.

        Returns:
            A new Response.
        """

        method = method.lower()

        response = await self.session.request(
            method=method,
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            allow_redirects=allow_redirects,
            timeout=timeout
        )

        if skip_roblox:
            # Skip parsing of this request. Return the response plain.
            return response

        # if we should handle the xcsrf, the xcsrf is in the response headers, and this method requires xcsrf handling
        if handle_xcsrf_token and self.xcsrf_token_name in response.headers and self.xcsrf_allowed_methods.get(method):
            self.session.headers[self.xcsrf_token_name] = response.headers[self.xcsrf_token_name]
            if response.status_code == 403:
                # 403 responses mean we have to send the request again because this token became invalid
                response = await self.session.request(
                    method=method,
                    url=url,
                    content=content,
                    data=data,
                    files=files,
                    json=json,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    auth=auth,
                    allow_redirects=allow_redirects,
                    timeout=timeout
                )

        if response.is_error:
            # Something went wrong, parse an error
            content_type = response.headers.get("Content-Type")
            errors = None

            if content_type and content_type.startswith("application/json"):
                # only parse JSON responses
                data = None

                try:
                    data = response.json()
                except JSONDecodeError:
                    pass

                errors = data and data.get("errors")

            # generate an exception from this status code
            exception = get_exception_from_status_code(response.status_code)(
                response=response,
                errors=errors
            )

            # raise the error
            raise exception
        else:
            return response

    async def get(
            self,
            url: URLTypes,
            *,
            params: QueryParamTypes = None,
            headers: HeaderTypes = None,
            cookies: CookieTypes = None,
            auth: Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
            allow_redirects: Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
            timeout: Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
    ) -> Response:
        """
        Sends a GET request.

        Returns:
            Response
        """

        return await self.request(
            method="GET",
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            allow_redirects=allow_redirects,
            timeout=timeout,
        )

    async def post(
            self,
            url: URLTypes,
            *,
            content: RequestContent = None,
            data: RequestData = None,
            files: RequestFiles = None,
            json: Any = None,
            params: QueryParamTypes = None,
            headers: HeaderTypes = None,
            cookies: CookieTypes = None,
            auth: Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
            allow_redirects: Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
            timeout: Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
    ) -> Response:
        """
        Sends a POST request.

        Returns:
            Response
        """

        return await self.request(
            method="POST",
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            allow_redirects=allow_redirects,
            timeout=timeout
        )

    async def put(
            self,
            url: URLTypes,
            *,
            content: RequestContent = None,
            data: RequestData = None,
            files: RequestFiles = None,
            json: Any = None,
            params: QueryParamTypes = None,
            headers: HeaderTypes = None,
            cookies: CookieTypes = None,
            auth: Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
            allow_redirects: Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
            timeout: Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
    ) -> Response:
        """
        Sends a PUT request.

        Returns:
            Response
        """

        return await self.request(
            method="PUT",
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            allow_redirects=allow_redirects,
            timeout=timeout
        )

    async def patch(
            self,
            url: URLTypes,
            *,
            content: RequestContent = None,
            data: RequestData = None,
            files: RequestFiles = None,
            json: Any = None,
            params: QueryParamTypes = None,
            headers: HeaderTypes = None,
            cookies: CookieTypes = None,
            auth: Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
            allow_redirects: Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
            timeout: Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
    ) -> Response:
        """
        Sends a PATCH request.

        Returns:
            Response
        """

        return await self.request(
            method="PATCH",
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            allow_redirects=allow_redirects,
            timeout=timeout
        )

    async def delete(
            self,
            url: URLTypes,
            *,
            params: QueryParamTypes = None,
            headers: HeaderTypes = None,
            cookies: CookieTypes = None,
            auth: Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
            allow_redirects: Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
            timeout: Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
    ) -> Response:
        """
        Sends a DELETE request.

        Returns:
            Response
        """

        return await self.request(
            method="DELETE",
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            allow_redirects=allow_redirects,
            timeout=timeout,
        )
