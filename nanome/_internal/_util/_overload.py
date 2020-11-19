import inspect


class overload (object):
    def __get__(self, instance, owner):
        self.obj = instance
        print("Agent %s called from %s " % (id(self), instance.name))
        return self

    def __init__(self, f):
        self.cases = {}
        self.alternate(f)

    def alternate(self, g):
        print(g)
        signature = inspect.getargspec(g).args
        self.cases[len(signature)] = g
        print(len(signature))
        print(self.cases)
        return self

    def __call__(self, *args):
        print(self.cases)
        print(args)
        print(self)
        function = self.cases[len(args) + 1]
        print(function)
        return function(self.obj, *args)


class Files(object):
    def __init__(self):
        self.name = "fred"

    @overload
    def ls(self, s):
        '''
         test
        '''
        print("1 arg version")

    @ls.alternate
    def ls(self, path, pattern):
        '''
         test test dude it woooorks.
         well done!
        '''
        print("2 arg version")


f = Files()

print("--------------testing-----------------")
f.ls("s")
f.ls("s", "t")
f.ls()
