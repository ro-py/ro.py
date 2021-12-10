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
        super().__init__(shared=shared, asset_id=data["AssetId"])

        self.id: int = data["AssetId"]
        self.name: str = data["AssetName"]

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name!r}>"
