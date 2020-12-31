"""

This file houses functions and classes that pertain to the Roblox catalog.

"""

import enum


class AppStore(enum.Enum):
    """
    Represents an app store that the Roblox app is downloadable on.
    """
    google_play = "GooglePlay"
    android = "GooglePlay"
    amazon = "Amazon"
    fire = "Amazon"
    ios = "iOS"
    iphone = "iOS"
    idevice = "iOS"
    xbox = "Xbox"
