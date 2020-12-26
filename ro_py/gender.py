"""

I hate how Roblox stores gender at all, it's really strange as it's not used for anything.
There's literally no point in storing this information.

"""

import enum


class RobloxGender(enum.Enum):
    """
    Represents the gender of the authenticated Roblox client.
    """
    Other = 1
    Female = 2
    Male = 3
