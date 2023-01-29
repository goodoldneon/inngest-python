from typing import Callable

from inngest.components.inngest_function import InngestFunction


def create_function(
    name: str,
    event: str,
    fn: Callable,
) -> InngestFunction:
    return InngestFunction(
        {"name": name},
        {"event": event},
        fn,
    )


__all__ = ["create_function"]
