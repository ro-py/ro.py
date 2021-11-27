"""

Contains types used internally by ro.py.

"""

from typing import Union

from ..bases.baseasset import BaseAsset
from ..bases.basebadge import BaseBadge
from ..bases.basegamepass import BaseGamePass
from ..bases.basegroup import BaseGroup
from ..bases.baseplace import BasePlace
from ..bases.baserole import BaseRole
from ..bases.baseuniverse import BaseUniverse
from ..bases.baseuser import BaseUser

AssetOrAssetId = Union[BaseAsset, int]
BadgeOrBadgeId = Union[BaseBadge, int]
GamePassOrGamePassId = Union[BaseGamePass, int]
GroupOrGroupId = Union[BaseGroup, int]
PlaceOrPlaceId = Union[BasePlace, int]
UniverseOrUniverseId = Union[BaseUniverse, int]
UserOrUserId = Union[BaseUser, int]
RoleOrRoleId = Union[BaseRole, int]
