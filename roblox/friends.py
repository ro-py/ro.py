from .utilities.shared import ClientSharedObject

from .users import User


class Friend(User):
    def __init__(self, shared: ClientSharedObject, data: dict):
        super().__init__(shared=shared, data=data)

        self.is_online: bool = data["isOnline"]
        self.presence_type: int = data["presenceType"]
        self.is_deleted: bool = data["isDeleted"]
        self.friend_frequent_rank: int = data["friendFrequentRank"]
