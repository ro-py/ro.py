from ..utilities.shared import ClientSharedObject


class BaseJob:
    def __init__(self, shared: ClientSharedObject, job_id: str):
        self._shared: ClientSharedObject = shared
        self.id: str = job_id
