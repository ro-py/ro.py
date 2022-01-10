"""

Contains the Shout object, which represents a group's shout.

"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client
from datetime import datetime

from dateutil.parser import parse

from .partials.partialuser import PartialUser


class Shout:
    """
    Represents a Group Shout.

    Attributes:
        body: The text of the shout.
        created: When the shout was created.
        updated: When the shout was updated.
        poster: Who posted the shout.
    """

    def __init__(
            self,
            client: Client,
            data: dict
    ):
        """
        Arguments:
            client: Client object.
            data: The data from the request.
        """
        self._client: Client = client

        self.body: str = data["body"]
        self.created: datetime = parse(data["created"])
        self.updated: datetime = parse(data["updated"])
        self.poster: PartialUser = PartialUser(
            client=self._client,
            data=data["poster"]
        )

    def __repr__(self):
        return f"<{self.__class__.__name__} created={self.created} updated={self.updated} body={self.body!r} " \
               f"poster={self.poster!r}>"
