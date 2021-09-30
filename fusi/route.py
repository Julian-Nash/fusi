from typing import Callable, Sequence


class Route:

    __slots__ = "_name", "_pattern", "_handler", "_methods"

    def __init__(self, name: str, pattern: str, handler: Callable, methods: Sequence[str]):
        self._name = name
        self._pattern = pattern
        self._handler = handler
        self._methods: tuple = tuple(set(i.upper() for i in methods))

    @property
    def name(self):
        return self._name

    @property
    def pattern(self):
        return self._pattern

    @property
    def handler(self):
        return self._handler

    @property
    def methods(self):
        return self._methods

    def __repr__(self):
        return (
            f"Route(name='{self.name}', pattern='{self.pattern}', "
            f"handler='{self.handler.__name__}' methods={self.methods})"
        )
