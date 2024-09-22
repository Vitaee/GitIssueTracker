import asyncio
from functools import wraps
from celery import Celery, Task
from typing import Any, Callable, Coroutine, ParamSpec, TypeVar

_P = ParamSpec("_P")
_R = TypeVar("_R")


def async_task(app: Celery, *args: Any, **kwargs: Any):
    def _decorator(func: Callable[_P, Coroutine[Any, Any, _R]]) -> Task:
        @app.task(*args, **kwargs)
        @wraps(func)
        def _decorated(*args: _P.args, **kwargs: _P.kwargs) -> _R:
            # Use asyncio.run() to run the async function in a sync Celery task
            return asyncio.run(func(*args, **kwargs))

        return _decorated

    return _decorator