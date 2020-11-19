import functools
import inspect
from functools import wraps

class overload (object):
    def __get__(self, instance, owner):
        self.obj = instance
        return self

    def __init__(self, f):
        self.cases = {}
        signature = inspect.getargspec(f).args
        self.cases[len(signature)] = f
        self.method = f

    def alternate(self):
        def alternate_decorator(f):
            @wraps(f)
            def wrapper(f):
                signature = inspect.getargspec(f).args
                self.cases[len(signature)] = f
                return self
            # functools.update_wrapper(store_function, self.f)
            return wrapper
        return alternate_decorator

    def __call__(self, *args):
        function = self.cases[len(args) + 1]
        return function(self.obj, *args)


class Files(object):
    def __init__(self):
        self.name = "fred"

    @overload
    def ls(self, path, pattern):
        '''
         test test dude it woooorks.
         well done!
        '''
        print("2 arg version")

    @ls.alternate
    def ls(self, s):
        '''
         test
        '''
        print("1 arg version")

f = Files()

print("--------------testing-----------------")
f.ls("s")
f.ls("s", "t")