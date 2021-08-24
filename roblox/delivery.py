from .utilities.shared import ClientSharedObject
from .utilities.url import cdn_site


class DeliveryProvider:
    def __init__(self, shared: ClientSharedObject):
        self._shared: ClientSharedObject = shared

    def get_hash_cdn(self, hash: str) -> int:
        """
        Returns the CDN number for the given Roblox CDN hash.
        """
        i = 31
        for char in hash[:32]:
            i ^= ord(char)  # i ^= int(char, 16) also works
        return i % 8

    def get_hash_url(self, hash: str) -> str:
        """
        Returns the full URL for the given Roblox CDN hash.
        """
        cdn: int = self.get_hash_cdn(hash)
        url: str = self._shared.url_generator.get_url(f"t{cdn}", hash, cdn_site)
        return url
