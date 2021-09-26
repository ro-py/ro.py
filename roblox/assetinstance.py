from .utilities.shared import ClientSharedObject
from .bases.baseasset import BaseAsset
from .bases.baseassetinstance import BaseAssetInstance


class AssetInstance(BaseAssetInstance):
    """
    Attributes:
        _data: The data we get back from the endpoint.
        _shared: The shared object, which is passed to all objects this client generates.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            shared: The ClientSharedObject.
            data: The data from the endpoint.
        """
        self._shared: ClientSharedObject = shared
        self._data: dict = data

        # TODO: add the type here and make this a generic instance object (i guess?)
        self.asset: BaseAsset = BaseAsset(
            shared=self._shared,
            asset_id=data["id"]
        )

        super().__init__(shared=shared, asset_instance_id=data["instanceId"])

        self.name: str = data["name"]
