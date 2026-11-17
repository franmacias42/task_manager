import logging
from collections.abc import Callable
from functools import wraps
from time import perf_counter
from typing import Any, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])

logger = logging.getLogger(__name__)


def measure_execution_time(func: F) -> F:
    """Measure and log the execution time of a function."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter()

        try:
            return func(*args, **kwargs)
        finally:
            elapsed_time = perf_counter() - start_time

            logger.info(
                "Function %s executed in %.6f seconds",
                func.__qualname__,
                elapsed_time,
            )

    return cast(F, wrapper)
