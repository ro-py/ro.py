"""

Contains shared enums.
fixme: this should be deprecated!

"""

from enum import Enum


class CreatorType(Enum):
    """
    Represents the type of creator for objects that can be owned by either a group or a user, like Assets.

    Attributes:
        group: The creater is a group.
        user: The creator is a user.
    """

    group = "Group"
    user = "User"
