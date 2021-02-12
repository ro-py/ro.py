"""

This file houses functions and classes that pertain to events and event handling with ro.py. Most methods that have
events actually don't reference content here, this doesn't contain much at the moment.

"""

import enum


class EventTypes(enum.Enum):
    on_join_request = "on_join_request"
    on_wall_post = "on_wall_post"
    on_group_change = "on_group_change"
    on_asset_change = "on_asset_change"
    on_user_change = "on_user_change"
    on_audit_log = "on_audit_log"
    on_trade_request = "on_trade_request"
