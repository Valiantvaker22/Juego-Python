"""
EventBus - Simple publish/subscribe for decoupled communication.

Usage:
    bus.subscribe("balloon_popped", my_callback)
    bus.emit("balloon_popped", balloon=balloon_obj, gold=2)
"""

from collections import defaultdict
from typing import Callable


class EventBus:
    def __init__(self):
        self._listeners: dict[str, list[Callable]] = defaultdict(list)

    def subscribe(self, event: str, callback: Callable):
        self._listeners[event].append(callback)

    def unsubscribe(self, event: str, callback: Callable):
        self._listeners[event] = [
            cb for cb in self._listeners[event] if cb != callback
        ]

    def emit(self, event: str, **kwargs):
        for cb in self._listeners[event]:
            cb(**kwargs)

    def clear(self):
        self._listeners.clear()
