import asyncio
from functools import wraps
from celery import Celery, Task
from typing import Any, Callable, Coroutine, ParamSpec, TypeVar
import threading
import concurrent.futures

_P = ParamSpec("_P")
_R = TypeVar("_R")


def async_task(app: Celery, *args: Any, **kwargs: Any):
    """
    Advanced async task decorator that properly handles asyncio in Celery tasks.
    
    This implementation uses a thread pool executor to avoid blocking the main thread
    and properly manages event loops for async functions.
    """
    def _decorator(func: Callable[_P, Coroutine[Any, Any, _R]]) -> Task:
        @app.task(*args, **kwargs)
        @wraps(func)
        def _decorated(*args: _P.args, **kwargs: _P.kwargs) -> _R:
            # Check if there's already a running event loop
            try:
                loop = asyncio.get_running_loop()
                # If there's a running loop, we're in an async context
                # Use a thread pool executor to run the async function
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, func(*args, **kwargs))
                    return future.result()
            except RuntimeError:
                # No running loop, safe to use asyncio.run()
                return asyncio.run(func(*args, **kwargs))

        return _decorated

    return _decorator