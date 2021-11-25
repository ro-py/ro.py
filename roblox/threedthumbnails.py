"""
Contains classes related to 3D thumbnails.
"""

from typing import List

from .delivery import ThumbnailCDNHash
from .utilities.shared import ClientSharedObject


class ThreeDThumbnailVector3:
    """
    Represents a Vector3 used in a 3D thumbnail.

    Attributes:
        x: The X component of the vector.
        y: The Y component of the vector.
        z: The Z component of the vector.
    """

    def __init__(self, data: dict):
        self.x: float = data["x"]
        self.y: float = data["y"]
        self.z: float = data["z"]


class ThreeDThumbnailCamera:
    """
    Represents a camera in a 3D thumbnail.

    Attributes:
        fov: The camera's field of view.
        position: The camera's position.
        direction: The camera's direction.
    """

    def __init__(self, data: dict):
        self.fov: float = data["fov"]
        self.position: ThreeDThumbnailVector3 = ThreeDThumbnailVector3(data["position"])
        self.direction: ThreeDThumbnailVector3 = ThreeDThumbnailVector3(data["direction"])


class ThreeDThumbnailAABB:
    """
    Represents AABB data in a 3D thumbnail.
    Roblox uses this data to calculate the maximum render distance used when rendering 3D thumbnails.
    ```js
    THREE.Vector3(json.aabb.max.x, json.aabb.max.y, json.aabb.max.z).length() * 4;
    ```

    Attributes:
        min: The minimum render position.
        max: The maximum render position.
    """

    def __init__(self, data: dict):
        self.min: ThreeDThumbnailVector3 = ThreeDThumbnailVector3(data["min"])
        self.max: ThreeDThumbnailVector3 = ThreeDThumbnailVector3(data["max"])


class ThreeDThumbnail:
    """
    Represents a user's 3D Thumbnail data.
    For more info, see https://robloxapi.wiki/wiki/3D_Thumbnails.

    Attributes:
        mtl: A CDN hash pointing to the MTL data.
        obj: A CDN hash pointing to the OBJ data.
        textures: A list of CDN hashes pointing to PNG texture data.
        camera: The camera object.
        aabb: The AABB object.
    """

    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared

        self.mtl: ThumbnailCDNHash = self._shared.delivery_provider.get_thumbnail_cdn_hash(data["mtl"])
        self.obj: ThumbnailCDNHash = self._shared.delivery_provider.get_thumbnail_cdn_hash(data["obj"])
        self.textures: List[ThumbnailCDNHash] = [
            self._shared.delivery_provider.get_thumbnail_cdn_hash(cdn_hash) for cdn_hash in data["textures"]
        ]
        self.camera: ThreeDThumbnailCamera = ThreeDThumbnailCamera(data["camera"])
        self.aabb: ThreeDThumbnailAABB = ThreeDThumbnailAABB(data["aabb"])
