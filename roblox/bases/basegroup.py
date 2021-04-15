class BaseGroup:
    """
    Represents a group with as little information possible.
    """
    def __init__(self, cso, group_id):
        self.cso = cso
        self.group_id = group_id

    def get_join_requests(self):
        pass
