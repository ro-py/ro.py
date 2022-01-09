"""

This file contains the BaseJob object, which represents a Roblox job ID.

"""

from __future__ import annotations
from typing import TYPE_CHECKING

from .baseitem import BaseItem

if TYPE_CHECKING:
    from ..client import Client


class BaseJob(BaseItem):
    """
    Represents Roblox job ID.

    Job IDs are UUIDs that represent a single game server instance.
    Learn more on the Developer Hub [here](https://developer.roblox.com/en-us/api-reference/property/DataModel/JobId).

    Attributes:
        id: The job ID.
    """

    def __init__(self, client: Client, job_id: str):
        """
        Arguments:
            client: The Client this object belongs to.
            job_id: The job ID.
        """

        self._client: Client = client
        self.id: str = job_id
