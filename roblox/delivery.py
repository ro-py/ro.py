"""

Contains classes and functions related to Roblox asset delivery.

"""

from .utilities.shared import ClientSharedObject
from .utilities.url import cdn_site


def get_cdn_number(hash: str) -> int:
    """
    Arguments:
        hash: The CDN hash to generate a CDN number for.

    Returns: The CDN number for the supplied hash.
    """
    i = 31
    for char in hash[:32]:
        i ^= ord(char)  # i ^= int(char, 16) also works
    return i % 8


class BaseHash:
    """
    Represents a hash on a Roblox content delivery network.

    Attributes:
        _shared: The shared object.
        hash: The hash as a string.
    """

    def __init__(self, shared: ClientSharedObject, hash: str):
        """
        Arguments:
            shared: The shared object.
            hash: The hash as a string.
        """

        self._shared: ClientSharedObject = shared
        self.hash: str = hash

    def get_cdn_number(self) -> int:
        """
        Returns the CDN number of this hash.
        """

        return get_cdn_number(self.hash)

    def _get_url(self, prefix: str, site: str = cdn_site) -> str:
        cdn_number: int = self.get_cdn_number()
        return self._shared.url_generator.get_url(f"{prefix}{cdn_number}", self.hash, site)

    def get_url(self, site: str = cdn_site) -> str:
        """
        Gets the hash's URL. This should be implemented by subclasses.
        """

        raise NotImplementedError


class ThumbnailHash(BaseHash):
    """
    Represents a hash on tX.rbxcdn.com.
    """

    def __init__(self, shared: ClientSharedObject, hash: str):
        super().__init__(shared=shared, hash=hash)

    def get_url(self, site: str = cdn_site) -> str:
        """
        Returns this hash's URL.
        """

        return self._get_url("t", cdn_site)


class ContentHash(BaseHash):
    """
    Represents a hash on cX.rbxcdn.com.
    """

    def __init__(self, shared: ClientSharedObject, hash: str):
        super().__init__(shared=shared, hash=hash)

    def get_url(self, site: str = cdn_site) -> str:
        """
        Returns this hash's URL.
        """

        return self._get_url("c", cdn_site)


class DeliveryProvider:
    """
    Attributes:
        _shared: The shared object, which is passed to all objects this client generates.
    """

    def __init__(self, shared: ClientSharedObject):
        """
        Arguments:
            shared: The shared object, which is passed to all objects this client generates.
        """
        self._shared: ClientSharedObject = shared

    def get_hash(self, hash: str) -> BaseHash:
        """
        Gets a Roblox CDN hash.

        Arguments:
            hash: The hash.

        Returns: A BaseHash.
        """

        return BaseHash(
            shared=self._shared,
            hash=hash
        )

    def get_hash_from_url(self, url: str, site: str = cdn_site) -> BaseHash:
        """
        todo: turn this into something that actually splits into path.

        Arguments:
            url: A CDN url.
            site: The site this hash is located at.

        Returns: The CDN hash for the supplied CDN URL.
        """

        return self.get_hash(
            hash=url.split(f".{site}/")[1]
        )
