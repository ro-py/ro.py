"""

This extension houses functions that allow generation of Bot objects, which interpret commands.

"""


from ro_py.client import Client


class Bot(Client):
    def __init__(self):
        super().__init__()


class Command:
    def __init__(self):
        pass


def command(function):
    def decorator(func):
        if isinstance(func, Command):
            raise TypeError('Callback is already a command.')
        return Command(func, name=name, **attrs)

    return decorator
