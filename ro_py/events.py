"""

This file houses functions and classes that pertain to events and event handling with ro.py. Most methods that have
events actually don't reference content here, this doesn't contain much at the moment.

"""

import enum
import time
import asyncio
from typing import Callable, Tuple


class EventTypes(enum.Enum):
    on_join_request = "on_join_request"
    on_wall_post = "on_wall_post"
    on_group_change = "on_group_change"
    on_asset_change = "on_asset_change"
    on_user_change = "on_user_change"
    on_audit_log = "on_audit_log"
    on_trade_request = "on_trade_request"


class Event:
    def __init__(self, func: Callable, event_type: EventTypes, arguments: Tuple = (), delay: int = 15):
        self.function = func
        self.event_type = event_type
        self.arguments = arguments
        self.delay = delay
        self.next_run = time.time() + delay

    def edit(self, arguments: Tuple = None, delay: int = None, func: Callable = None):
        self.arguments = arguments if arguments else self.arguments
        self.delay = delay if delay else self.delay
        self.function = func if func else self.function


class EventHandler:
    def __init__(self):
        self.events = []
        self.running = False

    def add_event(self, event: Event):
        self.events.append(event)

    def print_events(self):
        text = "These are the current running events:"
        for event in self.events:
            text += f"\n{event.event_id}:\n   Next run: {event.next_run}\n   Times run per minute: {60 / event.delay}"
        print(text)

    async def stop_event(self, event: Event):
        self.events.remove(event)

    async def listen(self):
        if not self.running:
            self.running = True
            while True:
                # Limits delay to 1 second.
                await asyncio.sleep(1)
                for event in self.events:
                    if event.next_run <= time.time():
                        if not isinstance(event.arguments[-1], Event):
                            event.arguments = (*event.arguments, event)
                        asyncio.create_task(event.function(*event.arguments))
                        event.next_run = time.time() + event.delay
