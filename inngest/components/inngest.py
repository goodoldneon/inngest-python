from typing import Callable

from .inngest_function import InngestFunction

Fn = Callable[[dict], None]


class Inngest:
    def create_function(
        self,
        name: str,
        event: str,
        fn: Fn,
    ) -> InngestFunction:
        pass


__all__ = ["Inngest"]