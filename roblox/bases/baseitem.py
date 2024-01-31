"""

This file contains the BaseItem class, which all bases inherit.

"""


class BaseItem:
    """
    This object represents a base Roblox item. All other bases inherit this object.
    This object overrides equals and not-equals methods ensuring that two bases with the same ID are always equal.
    """
    id = None

    def __repr__(self):
        attributes_repr = "".join(f" {key}={value!r}" for key, value in self.__dict__.items() if not key.startswith("_"))
        return f"<{self.__class__.__name__}{attributes_repr}>"

    def __int__(self):
        return self.id

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.id == self.id

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return other.id != self.id
        return True
