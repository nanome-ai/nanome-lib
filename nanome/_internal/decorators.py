import functools
import logging

logger = logging.getLogger(__name__)


def deprecated(new_func=None, msg=""):
    def deprecated_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not wrapper.used:
                warning = "Function " + func.__name__ + " is deprecated. "
                if new_func is not None:
                    warning += "Try using " + new_func + " instead. "
                warning += msg
                logger.warning(warning)
                wrapper.used = True
            return func(*args, **kwargs)
        wrapper.used = False
        return wrapper
    return deprecated_decorator
