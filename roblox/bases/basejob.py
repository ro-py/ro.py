"""

This file contains the BaseJob object, which represents a Roblox job ID.

"""

from .baseitem import BaseItem
from ..utilities.shared import ClientSharedObject


class BaseJob(BaseItem):
    """
    Represents Roblox job ID.

    Job IDs are UUIDs that represent a single game server instance.
    Learn more on the Developer Hub [here](https://developer.roblox.com/en-us/api-reference/property/DataModel/JobId).

    Attributes:
        _shared: The ClientSharedObject.
        id: The job ID.
    """

    def __init__(self, shared: ClientSharedObject, job_id: str):
        """
        Arguments:
            shared: The ClientSharedObject.
            job_id: The job ID.
        """

        self._shared: ClientSharedObject = shared
        self.id: str = job_id
