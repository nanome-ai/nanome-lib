import asyncio
import logging
import sys


if sys.version_info >= (3, 4):
    # asyncio.coroutine is not available before Python 3.4,
    # so only import if we're in a compatible python version
    def handle_exception(exc_type, exc_value, exc_traceback):
        """Make sure uncaught exceptions are logged."""
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger = logging.getLogger('plugin')
        msg = "Uncaught " + exc_type.__name__
        logger.error(msg, exc_info=1)

    @asyncio.coroutine
    def exception_wrapper(fn, args, kwargs):
        """Wrap all callbacks to catch exceptions.

        Based on this documentation
        https://docs.python.org/3.6/library/asyncio-dev.html?highlight=exception#detect-exceptions-never-consumed
        """
        try:
            for fut in fn(*args, **kwargs):
                yield fut
            # yield from fn(*args, **kwargs)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            handle_exception(exc_type, exc_value, exc_traceback)

    def async_callback(fn):
        def task(*args, **kwargs):
            fut = asyncio.ensure_future(exception_wrapper(fn, args, kwargs))
            return fut
        return task
