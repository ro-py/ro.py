"""

ro.py > catalog.py

This file houses functions and classes that pertain to the Roblox catalog.

"""

import enum


class AppStore(enum.Enum):
    google_play = "GooglePlay"
    amazon = "Amazon"
    ios = "iOS"
    xbox = "Xbox"
