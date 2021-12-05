"""

ro.py  
A modern, asynchronous wrapper for the Roblox web API.

Copyright 2020-present jmkdev  
License: MIT, see LICENSE

"""

# Find the original here: https://github.com/Rapptz/discord.py/blob/master/discord/__init__.py

__title__ = "roblox"
__author__ = "jmkdev"
__license__ = "MIT"
__copyright__ = "Copyright 2020-present jmkdev"
__version__ = "2.0.0"

import logging
from typing import NamedTuple

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from .client import Client
from .utilities.exceptions import *
from .utilities.types import *
from .thumbnails import ThumbnailState, ThumbnailFormat, ThumbnailReturnPolicy, AvatarThumbnailType
from .universes import UniverseGenre, UniverseAvatarType
from .creatortype import CreatorType


class VersionInfo(NamedTuple):
    """
    Represents the package's version info.
    """
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(
    major=2,
    minor=0,
    micro=0,
    releaselevel="release",
    serial=0
)

logging.getLogger(__name__).addHandler(logging.NullHandler())
