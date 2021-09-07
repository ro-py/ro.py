from .utilities.shared import ClientSharedObject
from .utilities.url import cdn_site


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
            hash: The has you want the cdn number of.

        Returns:
            cdn number
        """
        i = 31
        for char in hash[:32]:
            i ^= ord(char)  # i ^= int(char, 16) also works
        return i % 8

    def get_hash_url(self, hash: str) -> str:
        """
        Arguments:
            hash: The has you want the cdn number of.

        Returns:
           full URL for the given Roblox CDN hash.
        """
        cdn: int = self.get_hash_cdn(hash)
        url: str = self._shared.url_generator.get_url(f"t{cdn}", hash, cdn_site)
        return url

    def get_hash_from_url(self, url: str) -> str:
        """
        Arguments:
            url: The url you want to get the hash from.

        Returns:
           hash for the given Roblox CDN url.
        """
        return url.split(f"{cdn_site}/")[1]
