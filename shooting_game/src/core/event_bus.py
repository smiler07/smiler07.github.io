from collections import defaultdict
from typing import Any, Callable


class EventBus:
    def __init__(self) -> None:
        self._listeners: dict[str, list[Callable]] = defaultdict(list)

    def on(self, event: str, callback: Callable) -> None:
        self._listeners[event].append(callback)

    def emit(self, event: str, **kwargs: Any) -> None:
        for cb in self._listeners[event]:
            cb(**kwargs)

    def clear(self) -> None:
        self._listeners.clear()
