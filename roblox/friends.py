from .utilities.shared import ClientSharedObject

from .users import User


class Friend(User):
    """
    Represents a Join Request

    Attributes:
        is_online: Is the player currently online?
        presence_type: Unknown
        is_deleted: Is your friend account deleted
        friend_frequent_rank: Unknown
    """
    def __init__(self, shared: ClientSharedObject, data: dict):
        """
        Arguments:
            data: The data we get back from the endpoint.
            shared: The shared object, which is passed to all objects this client generates.
        """
        super().__init__(shared=shared, data=data)

        self.is_online: bool = data["isOnline"]
        self.presence_type: int = data["presenceType"]
        self.is_deleted: bool = data["isDeleted"]
        self.friend_frequent_rank: int = data["friendFrequentRank"]
