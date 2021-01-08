"""

This extension houses functions that allow generation of Bot objects, which interpret commands.

"""


from ro_py.client import Client
import asyncio


class Bot(Client):
    def __init__(self):
        super().__init__()


class Command:
    def __init__(self, func, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError('Callback must be a coroutine.')


def command(function, **attrs):
    def decorator(func):
        if isinstance(func, Command):
            raise TypeError('Callback is already a command.')
        return Command(func, **attrs)

    return decorator
