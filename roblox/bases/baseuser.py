class BaseUser:
    """
    Represents a user with as little information possible.
    """
    def __init__(self, cso, user_id):
        self.cso = cso
        """A client shared object."""
        self.id = user_id
        """The id of the user."""
