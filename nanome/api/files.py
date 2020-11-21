import os
from typing import Callable
from nanome._internal._files import _Files
from nanome.util import DirectoryRequestOptions, FileErrorCode
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
    def __init__(self, plugin_instance):
        self.plugin = plugin_instance

    def pwd(self, callback):
        """
        | Print the full filename of the current working directory
        :param callback: function that will be called with the full filename
        :type Callable
        """
        id = self.plugin._network._send(_Messages.ls, None, callback != None)
        self.plugin._save_callback(id, callback)

    def cd(self, directory, callback):
        """
        | changes current directory
        :param directory: directory to change to. Supports pattern matching.
        :type directory: str
        :param callback: called when operation is completed with any potential errors.
        :type Callable
        """
        id = self.plugin._network._send(_Messages.ls, directory, callback != None)
        self.plugin._save_callback(id, callback)

    def ls(self, directory, callback):
        """
        | list directory contents
        :param directory: directory to request. Supports pattern matching.
        :type directory: str
        :param callback: function that will be called with contents of the directory
        :type Callable
        """
        id = self.plugin._network._send(_Messages.ls, directory, callback != None)
        self.plugin._save_callback(id, callback)

    def mv(self, source, dest, callback):
        """
        | Rename SOURCE to DEST, or move SOURCE(s) to directory DEST
        :param source: file to move or rename. Supports pattern matching.
        :type source: str
        :param dest: name or destination directory for the file
        :type dest: str
        :param callback: called when operation is completed with any potential errors.
        :type Callable
        """
        id = self.plugin._network._send(_Messages.ls, (source, dest), callback != None)
        self.plugin._save_callback(id, callback)

    def get(self, source, dest, callback):
        """
        | Moves a file from the nanome user to the a local directory
        :param source: file(s) to move. Supports pattern matching.
        :type source: str
        :param dest: local destination directory for the file
        :type dest: str
        :param callback: called when operation is completed with any potential errors.
        :type Callable
        """
        def cb(error, file):
            if (error == FileErrorCode.no_error):
                path = os.path.join(dest, file[0])
                data = file[1]
                with open(path, 'wb') as ofile:
                    ofile.write(data)
                    ofile.close()
            callback(error)
        id = self.plugin._network._send(_Messages.ls, source, True)
        self.plugin._save_callback(id, cb)

    def put(self, source, dest, callback):
        """
        | Moves a file from a local directory to the the nanome user
        :param source: local file(s) to move. Supports pattern matching.
        :type source: str
        :param dest: destination directory for the file
        :type dest: str
        :param callback: called when operation is completed with any potential errors.
        :type Callable
        """
        with open(source) as f:
            file = f.read()
            f.close()
        id = self.plugin._network._send(_Messages.ls, (dest, file), callback != None)
        self.plugin._save_callback(id, callback)

    def rm(self, target, callback):
        """
        | remove non-directory file
        :param directory: file to remove. Supports pattern matching.
        :type directory: str
        :param callback: called when operation is completed with any potential errors.
        :type Callable
        """
        id = self.plugin._network._send(_Messages.ls, target, callback != None)
        self.plugin._save_callback(id, callback)

    def rmdir(self, target, callback):
        """
        | remove directory
        :param directory: directory to remove. Supports pattern matching.
        :type directory: str
        :param callback: called when operation is completed with any potential errors.
        :type Callable
        """
        id = self.plugin._network._send(_Messages.ls, target, callback != None)
        self.plugin._save_callback(id, callback)