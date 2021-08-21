from datetime import datetime
from dateutil.parser import parse

from ..utilities.shared import ClientSharedObject
from ..bases.basegroup import BaseGroup


class PartialGroup(BaseGroup):
    def __init__(self, shared: ClientSharedObject, data: dict):
        super().__init__(shared, data["id"])

        self._shared: ClientSharedObject = shared
        self._data: dict = data

        self.id: int = data["id"]
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.member_count: str = data["memberCount"]
        self.public_entry_allowed: bool = data["publicEntryAllowed"]

        self.created: datetime = parse(data["created"])
        self.updated: datetime = parse(data["updated"])
