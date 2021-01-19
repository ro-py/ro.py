import enum


class EventTypes(enum.Enum):
    on_join_request = "on_join_request"
    on_wall_post = "on_wall_post"
    on_shout_update = "on_shout_update"
