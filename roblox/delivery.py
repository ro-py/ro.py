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
    def __init__(self, shared: ClientSharedObject, hash: str):
        self._shared: ClientSharedObject = shared
        self.hash: str = hash

    def get_cdn_number(self) -> int:
        return get_cdn_number(self.hash)

    def _get_url(self, prefix, site: str = cdn_site) -> str:
        cdn_number: int = self.get_cdn_number()
        return self._shared.url_generator.get_url(f"{prefix}{cdn_number}", self.hash, site)

    def get_url(self, site: str = cdn_site) -> str:
        raise NotImplementedError


class ThumbnailHash(BaseHash):
    def __init__(self, shared: ClientSharedObject, hash: str):
        super().__init__(shared=shared, hash=hash)

    def get_url(self, site: str = cdn_site) -> str:
        return self._get_url("t", cdn_site)


class ContentHash(BaseHash):
    def __init__(self, shared: ClientSharedObject, hash: str):
        super().__init__(shared=shared, hash=hash)

    def get_url(self, site: str = cdn_site) -> str:
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
        return BaseHash(
            shared=self._shared,
            hash=hash
        )

    def get_hash_from_url(self, url: str, site: str = cdn_site) -> BaseHash:
        """
        Arguments:
            url: A CDN url.

        Returns: The CDN hash for the supplied CDN URL.
        """
        print(site)
        return self.get_hash(
            hash=url.split(f".{site}/")[1]
        )
