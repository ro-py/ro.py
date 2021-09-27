from .utilities.shared import ClientSharedObject
from .utilities.url import cdn_site


def get_hash_from_url(url: str) -> str:
    """
    Arguments:
        url: The CDN URL you wan the CDN hash for.

    Returns:
       The CDN hash for the supplied CDN URL.
    """
    return url.split(f"{cdn_site}/")[1]


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

    def get_hash_cdn(self, hash: str) -> int:
        """
        Arguments:
            hash: The CDN hash to generate a CDN number for.

        Returns:
            The CDN number for the supplied hash.
        """
        i = 31
        for char in hash[:32]:
            i ^= ord(char)  # i ^= int(char, 16) also works
        return i % 8

    def get_hash_url(self, hash: str) -> str:
        """
        Arguments:
            hash: The CDN hash you want the CDN URL for.

        Returns:
           The CDN URL for the supplied hash.
        """
        cdn: int = self.get_hash_cdn(hash)
        url: str = self._shared.url_generator.get_url(f"t{cdn}", hash, cdn_site)
        return url
