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

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.id == self.id

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return other.id != self.id
        return True
