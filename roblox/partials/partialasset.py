from typing import Optional, List

from .. import BaseAsset
from ..utilities.shared import ClientSharedObject


class PartialAsset(BaseAsset):
    """
    Attributes:
        id: Id of the Asset
        name: Name of the Asset
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on assets.
            data: The data from the request.
        """
        self.shared = shared
        self.id: int = data["AssetId"]
        super().__init__(shared=self.shared, asset_id=self.id)

        self.name: str = data["AssetName"]

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r}>"


class VersionPartialAsset(PartialAsset):
    """
    Attributes:
        id: Id of the Asset
        name: Name of the Asset
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on assets.
            data: The data from the request.
        """
        super().__init__(shared=shared, data=data)

        self.version_number: int = data["VersionNumber"]
        self.revert_version_number: Optional[int] = data.get("RevertVersionNumber")


class ActionsPartialAsset(PartialAsset):
    """
    Attributes:
        id: Id of the Asset
        name: Name of the Asset
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on assets.
            data: The data from the request.
        """
        super().__init__(shared=shared, data=data)

        self.Actions: List[int] = data["Actions"]
