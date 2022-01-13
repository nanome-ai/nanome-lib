import asyncio
# import json
import logging
import sys
# import traceback


LOGGER_NAME = 'plugin'


def handle_exception(exc_type, exc_value, exc_traceback):
    """Make uncaught exceptions are logged."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger = logging.getLogger(LOGGER_NAME)
    # traceback_str = json.dumps(traceback.format_exc())[1:-1]
    # logger.error(traceback_str, exc_info=(exc_type, exc_value, exc_traceback))
    logger.error("Uncaught Exception. Traceback will be included in the future.")


@asyncio.coroutine
def exception_wrapper(fn, args, kwargs):
    """Wrap all callbacks to catch exceptions.

    Based on documentation here
    https://docs.python.org/3.6/library/asyncio-dev.html?highlight=exception#detect-exceptions-never-consumed
    """
    try:
        yield from fn(*args, **kwargs)
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        handle_exception(exc_type, exc_value, exc_traceback)


def async_callback(fn):
    def task(*args, **kwargs):
        # loop = asyncio.get_running_loop()
        fut = asyncio.ensure_future(exception_wrapper(fn, args, kwargs))
        return fut
    return task
