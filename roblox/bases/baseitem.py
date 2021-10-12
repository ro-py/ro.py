"""
This file contains the BaseItem class, which all bases inherit.
"""


class BaseItem:
    """
    All bases inherit this class.
    """
    id = None

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"

    def __int__(self):
        return self.id
