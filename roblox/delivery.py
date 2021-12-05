"""

Contains classes and functions related to Roblox asset delivery.

"""

from .utilities.shared import ClientSharedObject
from .utilities.url import cdn_site


def get_cdn_number(cdn_hash: str) -> int:
    """
    Gets the number in the CDN where number represents X in tX.rbxcdn.com

    Arguments:
        cdn_hash: The CDN cdn_hash to generate a CDN number for.

    Returns: 
        The CDN number for the supplied cdn_hash.
    """
    i = 31
    for char in cdn_hash[:32]:
        i ^= ord(char)  # i ^= int(char, 16) also works
    return i % 8


class BaseCDNHash:
    """
    Represents a cdn_hash on a Roblox content delivery network.

    Attributes:
        cdn_hash: The CDN hash as a string.
    """

    def __init__(self, shared: ClientSharedObject, cdn_hash: str):
        """
        Arguments:
            shared: The shared object.
            cdn_hash: The CDN hash as a string.
        """

        self._shared: ClientSharedObject = shared
        self.cdn_hash: str = cdn_hash

    def __repr__(self):
        return f"<{self.__class__.__name__} cdn_hash={self.cdn_hash}>"

    def get_cdn_number(self) -> int:
        """
        Returns the CDN number of this CDN hash.

        Returns:
            The computed number of the given cdn_hash
        """

        return get_cdn_number(self.cdn_hash)

    def _get_url(self, prefix: str, site: str = cdn_site) -> str:
        cdn_number: int = self.get_cdn_number()
        return self._shared.url_generator.get_url(f"{prefix}{cdn_number}", self.cdn_hash, site)

    def get_url(self, site: str = cdn_site) -> str:
        """
        Gets the cdn_hash's URL. This should be implemented by subclasses.

        Arguments:
            site: Represents the URL for what site it should target, be it rbxcdn.com, or roblox.com etc.

        Returns:
            The computed URL from the given cdn_hash attribute.
        """

        raise NotImplementedError


class ThumbnailCDNHash(BaseCDNHash):
    """
    Represents a CDN hash on tX.rbxcdn.com.
    """

    def __init__(self, shared: ClientSharedObject, cdn_hash: str):
        super().__init__(shared=shared, cdn_hash=cdn_hash)

    def get_url(self, site: str = cdn_site) -> str:
        """
        Returns this CDN hash's URL.
        """

        return self._get_url("t", cdn_site)


class ContentCDNHash(BaseCDNHash):
    """
    Represents a CDN hash on cX.rbxcdn.com.
    """

    def __init__(self, shared: ClientSharedObject, cdn_hash: str):
        super().__init__(shared=shared, cdn_hash=cdn_hash)

    def get_url(self, site: str = cdn_site) -> str:
        """
        Returns:
            This hash's URL.
        """

        return self._get_url("c", cdn_site)


class DeliveryProvider:
    """
    Provides CDN hashes and other delivery-related objects.
    """

    def __init__(self, shared: ClientSharedObject):
        """
        Arguments:
            shared: The shared object, which is passed to all objects this client generates.
        """
        self._shared: ClientSharedObject = shared

    def get_cdn_hash(self, cdn_hash: str) -> BaseCDNHash:
        """
        Gets a Roblox CDN cdn_hash.

        Arguments:
            cdn_hash: The cdn_hash.

        Returns:
            A BaseCDNHash.
        """

        return BaseCDNHash(
            shared=self._shared,
            cdn_hash=cdn_hash
        )

    def get_cdn_hash_from_url(self, url: str, site: str = cdn_site) -> BaseCDNHash:
        """
        todo: turn this into something that actually splits into path.

        Arguments:
            url: A CDN url.
            site: The site this cdn_hash is located at.

        Returns:
            The CDN cdn_hash for the supplied CDN URL.
        """

        return self.get_cdn_hash(
            cdn_hash=url.split(f".{site}/")[1]
        )

    def get_thumbnail_cdn_hash(self, cdn_hash: str) -> ThumbnailCDNHash:
        """
        Gets a Roblox CDN cdn_hash.

        Arguments:
            cdn_hash: The cdn_hash.

        Returns:
            A ThumbnailCDNHash.
        """

        return ThumbnailCDNHash(
            shared=self._shared,
            cdn_hash=cdn_hash
        )

    def get_content_cdn_hash(self, cdn_hash: str) -> ContentCDNHash:
        """
        Gets a Roblox CDN cdn_hash.

        Arguments:
            cdn_hash: The cdn_hash.

        Returns:
            A ContentCDNHash.
        """

        return ContentCDNHash(
            shared=self._shared,
            cdn_hash=cdn_hash
        )
