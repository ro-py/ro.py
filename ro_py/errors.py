"""

ro.py > errors.py

This file houses custom exceptions unique to this module.

"""


class NotLimitedError(Exception):
    """Called when code attempts to read limited-only information."""
    pass


class InvalidIconSizeError(Exception):
    """Called when code attempts to pass in an improper size to a thumbnail function."""
    pass
