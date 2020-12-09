from nanome._internal._files import _Files
from nanome.util import FileErrorCode
from nanome._internal._network._commands._callbacks import _Messages

class Files(_Files):
    def __init__(self, plugin_instance):
        self.plugin = plugin_instance

    def pwd(self, callback):
        """
        | Print the full filename of the current working directory
        :param callback: function that will be called with the full filename
        :type callback: method (:class:`~nanome.util.file.FileError`, str) -> None
        """
        id = self.plugin._network._send(_Messages.print_working_directory, None, callback != None)
        self.plugin._save_callback(id, callback)

    def cd(self, directory, callback):
        """
        | changes current directory
        :param directory: directory to change to.
        :type directory: str
        :param callback: called when operation is completed with any potential errors.
        :type callback: method (:class:`~nanome.util.file.FileError`) -> None
        """
        id = self.plugin._network._send(_Messages.cd, directory, callback != None)
        self.plugin._save_callback(id, callback)

    def ls(self, directory, callback):
        """
        | list directory contents
        :param directory: directory to request.
        :type directory: str
        :param callback: function that will be called with contents of the directory
        :type callback: method (:class:`~nanome.util.file.FileError`, list of :class:`~nanome.util.file.FileMeta`) -> None
        """
        id = self.plugin._network._send(_Messages.ls, directory, callback != None)
        self.plugin._save_callback(id, callback)

    def mv(self, source, dest, callback):
        """
        | Rename SOURCE to DEST, or move SOURCE(s) to directory DEST
        :param source: file to move or rename.
        :type source: str
        :param dest: name or destination directory for the file
        :type dest: str
        :param callback: called when operation is completed with any potential errors.
        :type callback: method (:class:`~nanome.util.file.FileError`) -> None
        """
        id = self.plugin._network._send(_Messages.mv, (source, dest), callback != None)
        self.plugin._save_callback(id, callback)

    def get(self, source, dest, callback):
        """
        | Moves a file from the nanome user to the a local directory
        :param source: file(s) to move.
        :type source: str
        :param dest: local destination directory for the file
        :type dest: str
        :param callback: called with the path to the file and any potential errors
        :type callback: method (:class:`~nanome.util.file.FileError`, str) -> None
        """
        def cb(error, file):
            if (error == FileErrorCode.no_error):
                with open(dest, 'wb') as ofile:
                    ofile.write(file)
                    ofile.close()
            callback(error, dest)
        id = self.plugin._network._send(_Messages.get, source, True)
        self.plugin._save_callback(id, cb)

    def put(self, source, dest, callback):
        """
        | Moves a file from a local directory to the the nanome user
        :param source: local file(s) to move.
        :type source: str
        :param dest: destination directory for the file
        :type dest: str
        :param callback: called when operation is completed with any potential errors.
        :type callback: method (:class:`~nanome.util.file.FileError`) -> None
        """
        with open(source, "rb") as f:
            file = f.read()
            f.close()
        id = self.plugin._network._send(_Messages.put, (dest, file), callback != None)
        self.plugin._save_callback(id, callback)

    def rm(self, target, callback):
        """
        | remove non-directory file
        :param target: file to remove.
        :type target: str
        :param callback: called when operation is completed with any potential errors.
        :type callback: method (:class:`~nanome.util.file.FileError`) -> None
        """
        id = self.plugin._network._send(_Messages.rm, target, callback != None)
        self.plugin._save_callback(id, callback)

    def rmdir(self, target, callback):
        """
        | remove directory
        :param target: directory to remove.
        :type target: str
        :param callback: called when operation is completed with any potential errors.
        :type callback: method (:class:`~nanome.util.file.FileError`) -> None
        """
        id = self.plugin._network._send(_Messages.rmdir, target, callback != None)
        self.plugin._save_callback(id, callback)

    def cp(self, source, dest, callback):
        """
        | Copy SOURCE to DEST
        :param source: file to copy.
        :type source: str
        :param dest: desired path for the copy
        :type dest: str
        :param callback: called when operation is completed with any potential errors.
        :type callback: method (:class:`~nanome.util.file.FileError`) -> None
        """
        id = self.plugin._network._send(_Messages.cp, (source, dest), callback != None)
        self.plugin._save_callback(id, callback)

    def mkdir(self, target, callback):
        """
        | Create the DIRECTORY(ies), if they do not already exist. 
        :param target: directory to create.
        :type target: str
        :param callback: called when operation is completed with any potential errors.
        :type callback: method (:class:`~nanome.util.file.FileError`) -> None
        """
        id = self.plugin._network._send(_Messages.mkdir, target, callback != None)
        self.plugin._save_callback(id, callback)