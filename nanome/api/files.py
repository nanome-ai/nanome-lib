from nanome._internal._files import _Files
from nanome.util import FileErrorCode
from nanome.util.enums import Permissions
from nanome._internal._network._commands._callbacks import _Messages


class Files(_Files):
    """
    | Class to navigate through files and directories on the machine running Nanome using unix-like filesystem methods.
    """

    def __init__(self, plugin_instance):
        self.plugin = plugin_instance

    def pwd(self, callback=None):
        """
        | Print the absolute path of the current working directory

        :param callback: function that will be called with the full working directory path
        :type callback: method (:class:`~nanome.util.file.FileError`, str) -> None
        """
        if not self.plugin._has_permission(Permissions.local_files_access):
            raise Exception("Plugin requires files permission to use this method.")
        expects_response = callback is not None or self.plugin.is_async
        id = self.plugin._network._send(_Messages.print_working_directory, None, expects_response)
        return self.plugin._save_callback(id, callback)

    def cd(self, directory, callback=None):
        """
        | changes the current working directory

        :param directory: directory to change to
        :type directory: str
        :param callback: called when operation has completed, potentially with errors
        :type callback: method (:class:`~nanome.util.file.FileError`) -> None
        """
        if not self.plugin._has_permission(Permissions.local_files_access):
            raise Exception("Plugin requires files permission to use this method.")
        expects_response = callback is not None or self.plugin.is_async
        id = self.plugin._network._send(_Messages.cd, directory, expects_response)
        return self.plugin._save_callback(id, callback)

    def ls(self, directory, callback=None):
        """
        | list directory's contents

        :param directory: directory to request
        :type directory: str
        :param callback: function that will be called with contents of the directory
        :type callback: method (:class:`~nanome.util.file.FileError`, list of :class:`~nanome.util.file.FileMeta`) -> None
        """
        if not self.plugin._has_permission(Permissions.local_files_access):
            raise Exception("Plugin requires files permission to use this method.")
        expects_response = callback is not None or self.plugin.is_async
        id = self.plugin._network._send(_Messages.ls, directory, expects_response)
        return self.plugin._save_callback(id, callback)

    def mv(self, source, dest, callback=None):
        """
        | Rename source to dest, or move source into directory dest/

        :param source: file to move or rename
        :type source: str
        :param dest: file or pathname of the file's destination
        :type dest: str
        :param callback: called when operation has completed, potentially with errors
        :type callback: method (:class:`~nanome.util.file.FileError`) -> None
        """
        if not self.plugin._has_permission(Permissions.local_files_access):
            raise Exception("Plugin requires files permission to use this method.")
        expects_response = callback is not None or self.plugin.is_async
        id = self.plugin._network._send(_Messages.mv, (source, dest), expects_response)
        return self.plugin._save_callback(id, callback)

    def get(self, source, dest, callback=None):
        """
        | Gets file source from the Nanome session's machine and writes to dest of the plugin machine.

        :param source: Nanome machine filename of the file to move
        :type source: str
        :param dest: plugin machine filename for the file's destination
        :type dest: str
        :param callback: called when operation has completed, with dest and any potential errors
        :type callback: method (:class:`~nanome.util.file.FileError`, str) -> None
        """
        if not self.plugin._has_permission(Permissions.local_files_access):
            raise Exception("Plugin requires files permission to use this method.")

        def cb(error, file):
            if error == FileErrorCode.no_error:
                with open(dest, 'wb') as ofile:
                    ofile.write(file)
                    ofile.close()
            callback(error, dest)
        id = self.plugin._network._send(_Messages.get, source, True)
        result = self.plugin._save_callback(id, cb if callback else None)
        if callback is None and self.plugin.is_async:
            result.real_set_result = result.set_result
            result.set_result = lambda args: cb(*args)
            callback = lambda *args: result.real_set_result(args)
        return result

    def put(self, source, dest, callback=None):
        """
        | Send the file source on the plugin machine to be placed at dest on the Nanome session's machine.

        :param source: plugin machine filename of the file to send
        :type source: str
        :param dest: Nanome machine filename for the file's destination
        :type dest: str
        :param callback: called when operation has completed, potentially with errors
        :type callback: method (:class:`~nanome.util.file.FileError`) -> None
        """
        if not self.plugin._has_permission(Permissions.local_files_access):
            raise Exception("Plugin requires files permission to use this method.")
        with open(source, "rb") as f:
            file = f.read()
            f.close()
        expects_response = callback is not None or self.plugin.is_async
        id = self.plugin._network._send(_Messages.put, (dest, file), expects_response)
        return self.plugin._save_callback(id, callback)

    def rm(self, target, callback=None):
        """
        | remove non-directory file

        :param target: filepath of Nanome machine file to remove.
        :type target: str
        :param callback: called when operation has completed, potentially with errors
        :type callback: method (:class:`~nanome.util.file.FileError`) -> None
        """
        if not self.plugin._has_permission(Permissions.local_files_access):
            raise Exception("Plugin requires files permission to use this method.")
        expects_response = callback is not None or self.plugin.is_async
        id = self.plugin._network._send(_Messages.rm, target, expects_response)
        return self.plugin._save_callback(id, callback)

    def rmdir(self, target, callback=None):
        """
        | remove directory

        :param target: Nanome machine directory to remove.
        :type target: str
        :param callback: called when operation has completed, potentially with errors
        :type callback: method (:class:`~nanome.util.file.FileError`) -> None
        """
        if not self.plugin._has_permission(Permissions.local_files_access):
            raise Exception("Plugin requires files permission to use this method.")
        expects_response = callback is not None or self.plugin.is_async
        id = self.plugin._network._send(_Messages.rmdir, target, expects_response)
        return self.plugin._save_callback(id, callback)

    def cp(self, source, dest, callback=None):
        """
        | Copy source to dest

        :param source: the Nanome machine filename of the file to copy
        :type source: str
        :param dest: the Nanome machine filename to copy to
        :type dest: str
        :param callback: called when operation has completed, potentially with errors
        :type callback: method (:class:`~nanome.util.file.FileError`) -> None
        """
        if not self.plugin._has_permission(Permissions.local_files_access):
            raise Exception("Plugin requires files permission to use this method.")
        expects_response = callback is not None or self.plugin.is_async
        id = self.plugin._network._send(_Messages.cp, (source, dest), expects_response)
        return self.plugin._save_callback(id, callback)

    def mkdir(self, target, callback=None):
        """
        | Create all directories along the path provided

        :param target: pathname of the final directory to create
        :type target: str
        :param callback: called when operation has completed, potentially with errors
        :type callback: method (:class:`~nanome.util.file.FileError`) -> None
        """
        if not self.plugin._has_permission(Permissions.local_files_access):
            raise Exception("Plugin requires files permission to use this method.")
        expects_response = callback is not None or self.plugin.is_async
        id = self.plugin._network._send(_Messages.mkdir, target, expects_response)
        return self.plugin._save_callback(id, callback)
