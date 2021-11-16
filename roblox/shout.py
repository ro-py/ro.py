"""

Contains the Shout object, which represents a group's shout.

"""

from datetime import datetime

from dateutil.parser import parse

from .partials.partialuser import PartialUser
from .utilities.shared import ClientSharedObject


class Shout:
    """
    Represents a Group Shout.

    Attributes:
        _shared: The shared object, which is passed to all objects this client generates.
        body: The text of the shout.
        created: When the shout was created.
        updated: When the shout was updated.
        poster: Who posted the shout.
    """

    def __init__(
            self,
            shared: ClientSharedObject,
            data: dict
    ):
        """
        Arguments:
            shared: Shared object.
            data: The data from the request.
        """
        self._shared: ClientSharedObject = shared

        self.body: str = data["body"]
        self.created: datetime = parse(data["created"])
        self.updated: datetime = parse(data["updated"])
        self.poster: PartialUser = PartialUser(
            shared=self._shared,
            data=data["poster"]
        )

    def __repr__(self):
        return f"<{self.__class__.__name__} created={self.created} updated={self.updated} body={self.body!r} " \
               f"poster={self.poster!r}>"
