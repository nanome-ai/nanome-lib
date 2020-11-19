from typing import Callable
from nanome._internal._files import _Files
from nanome.util import DirectoryRequestOptions
from nanome._internal._network._commands._callbacks import _Messages

class overload:
    def __init__(self, f):
        self.cases = {}

    def args(self, *args):
        def store_function(f):
            self.cases[tuple(args)] = f
            return self
        return store_function

    def __call__(self, *args):
        function = self.cases[tuple(type(arg) for arg in args)]
        return function(*args)

class Files(_Files):
    def __init__(self):
        pass

    def pwd(self):
        pass

    def cd(self):
        pass

    @overload
    def ls(self): 
        pass

    @ls.args(str, str, Callable)
    def ls(self, path, pattern, callback):
        """
        | Requests the content of a directory on the machine running Nanome

        :param path: Path to request. E.g. "." means Nanome's running directory
        :type path: str
        :param pattern: Pattern to match. E.g. "*.txt" will match all .txt files. Default value is "*" (match everything)
        :type pattern: str
        """
        options = DirectoryRequestOptions()
        options._directory_name = path
        options._pattern = pattern
        id = self._network._send(_Messages.directory_request, options, callback != None)
        self._save_callback(id, callback)

    @ls.args(str, Callable)
    def ls(self, path, callback):
        pattern = "*"
        options = DirectoryRequestOptions()
        options._directory_name = path
        options._pattern = pattern
        id = self._network._send(_Messages.directory_request, options, callback != None)
        self._save_callback(id, callback)

    def mv(self):
        pass

    def get(self):
        pass

    def put(self):
        pass

    def rm(self):
        pass

    def rmdir(self):
        pass

f = Files()
f.ls()