from .partials.partialuser import PartialUser
from .partials.partialrole import PartialRole
from .utilities.shared import ClientSharedObject


class Member(PartialUser):
    def __init__(self, shared: ClientSharedObject, data: dict):
        self._shared: ClientSharedObject = shared

        super().__init__(shared=self._shared, data=data["user"])

        self.role: PartialRole = PartialRole(shared=self._shared, data=data["role"])
