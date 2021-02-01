import enum


class EventTypes(enum.Enum):
    on_join_request = "on_join_request"
    on_wall_post = "on_wall_post"
    on_group_change = "on_group_change"
    on_asset_change = "on_asset_change"
    on_user_change = "on_user_change"
    on_audit_log = "on_audit_log"
