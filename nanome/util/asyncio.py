import asyncio
import inspect
import logging
import sys
from concurrent.futures._base import CancelledError
from . import Logs


async def handle_exception(exc_type, exc_value, exc_traceback):
    """Make sure uncaught exceptions are logged."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    # Get the module where error originated from the traceback
    frm = inspect.trace()[-1]
    mod = inspect.getmodule(frm[0])
    mod_name = mod.__name__ if mod else frm[1]
    if mod_name:
        logger = logging.getLogger(mod_name)
    else:
        logger = logging.getLogger()

    msg = "Uncaught " + exc_type.__name__ + ": " + str(exc_value)
    logger.error(msg, exc_info=1)
    await asyncio.sleep(0.1)  # Give log a split second to process


async def exception_wrapper(fn, args, kwargs):
    """Wrap all callbacks to catch exceptions.

    Based on this documentation
    https://docs.python.org/3.6/library/asyncio-dev.html?highlight=exception#detect-exceptions-never-consumed
    """
    try:
        return await fn(*args, **kwargs)
    except CancelledError:
        # A user exiting and cancelling the request should not be logged as an error.
        Logs.message("Request was cancelled by the user.")
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        await handle_exception(exc_type, exc_value, exc_traceback)


def async_callback(fn):
    def task(*args, **kwargs):
        fut = asyncio.create_task(exception_wrapper(fn, args, kwargs))
        return fut
    return task
