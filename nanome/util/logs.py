import functools
import inspect
from .enum import IntEnum, auto
import logging


class Logs(object):
    """
    | Allows for easy message logging without buffer issues.
    | Possible log types are Debug, Warning, and Error.
    """
    class LogType(IntEnum):
        debug = auto()
        warning = auto()
        error = auto()
        info = auto()

    @classmethod
    def error(cls, *args):
        """
        | Prints an error

        :param args: Variable length argument list
        :type args: Anything printable
        """
        module = cls.caller_name()
        logger = logging.getLogger(module)
        msg = ' '.join(map(str, args))
        logger.error(msg)

    @classmethod
    def warning(cls, *args):
        """
        | Prints a warning

        :param args: Variable length argument list
        :type args: Anything printable
        """
        module = cls.caller_name()
        logger = logging.getLogger(module)
        msg = ' '.join(map(str, args))
        logger.warning(msg)

    @classmethod
    def message(cls, *args):
        """
        | Prints a message

        :param args: Variable length argument list
        :type args: Anything printable
        """
        module = cls.caller_name()
        logger = logging.getLogger(module)
        msg = ' '.join(map(str, args))
        logger.info(msg)

    @classmethod
    def debug(cls, *args):
        """
        | Prints a debug message
        | Prints only if plugin started in verbose mode (with -v argument)

        :param args: Variable length argument list
        :type args: Anything printable
        """
        module = cls.caller_name()
        logger = logging.getLogger(module)
        msg = ' '.join(map(str, args))
        logger.debug(msg)

    @staticmethod
    def deprecated(new_func=None, msg=""):
        def deprecated_decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if not wrapper.used:
                    warning = "Function " + func.__name__ + " is deprecated. "
                    if new_func is not None:
                        warning += "Try using " + new_func + " instead. "
                    warning += msg
                    Logs.warning(warning)
                    wrapper.used = True
                return func(*args, **kwargs)
            wrapper.used = False
            return wrapper
        return deprecated_decorator

    @staticmethod
    def caller_name(skip=2):
        """Get a name of a caller in the format module.class.method

        `skip` specifies how many levels of stack to skip while getting caller
        name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

        An empty string is returned if skipped levels exceed stack height

        https://stackoverflow.com/questions/2654113/how-to-get-the-callers-method-name-in-the-called-method
        """
        stack = inspect.stack()
        start = 0 + skip
        if len(stack) < start + 1:
            return ''
        parentframe = stack[start][0]

        name = []
        module = inspect.getmodule(parentframe)
        # `modname` can be None when frame is executed directly in console
        # TODO(techtonik): consider using __main__
        if module:
            name.append(module.__name__)
        # detect classname
        if 'self' in parentframe.f_locals:
            # I don't know any way to detect call from the object method
            # XXX: there seems to be no way to detect static method call - it will
            #      be just a function call
            name.append(parentframe.f_locals['self'].__class__.__name__)
        codename = parentframe.f_code.co_name
        if codename != '<module>':  # top level usually
            name.append(codename)  # function or a method

        # Avoid circular refs and frame leaks
        #  https://docs.python.org/2.7/library/inspect.html#the-interpreter-stack
        del parentframe, stack

        return ".".join(name)
