from . import IntEnum
from .enums import LoadFileErrorCode


class FileError(IntEnum):
    """
    | File errors encounterable after performing a file operation on the Nanome host machine.
    | Accessible via the first parameter of the 'done' callback for all methods on plugin_instance.files
    """
    no_error = 0,
    invalid_path = 1,
    io_error = 2,
    security_error = 3,
    unauthorized_access = 4


class FileMeta(object):
    """
    | Represents file metadata from a Nanome host machine.
    | Accessible via the second parameter of the 'done' callback for plugin_instance.files.ls
    """

    def __init__(self):
        self.name = ""
        self.size = 0
        self.date_modified = 0
        self.is_directory = False

# deprecated: This is part of the deprecated file API


class DirectoryErrorCode(IntEnum):
    """
    | Deprecated.
    """
    no_error = 0
    folder_unreachable = 1

# deprecated: This is part of the deprecated file API


class FileErrorCode(IntEnum):
    """
    | Deprecated.
    """
    no_error = 0
    file_unreachable = 1
    path_too_long = 2
    missing_permission = 3

# deprecated: This is part of the deprecated file API


class DirectoryEntry(object):
    """
    | Deprecated.
    """

    def __init__(self):
        self.name = ""
        self.is_directory = False

# deprecated: This is part of the deprecated file API


class FileData(object):
    """
    | Deprecated.
    """

    def __init__(self):
        self.data = None
        self.error_code = FileErrorCode.no_error

# deprecated: This is part of the deprecated file API


class FileSaveData(object):
    """
    | Deprecated.
    """

    def __init__(self):
        self.path = ""
        self.data = bytearray()
        self.error_code = FileErrorCode.no_error

    def write_text(self, text):
        self.data.extend(text.encode('ascii'))

# deprecated: This is part of the deprecated file API


class DirectoryRequestResult(object):
    """
    | Deprecated.
    """

    def __init__(self):
        self.entry_array = []
        self.error_code = DirectoryErrorCode.no_error

# deprecated: This is part of the deprecated file API


class DirectoryRequestOptions(object):
    """
    | Deprecated.
    """

    def __init__(self):
        self._directory_name = "."
        self._pattern = "*"


class LoadInfoDone():
    """
    | Represents the a file operation on the Nanome host machine.
    | Accessible via the first parameter of the 'done' callback for all methods on plugin_instance.files
    """
    ErrorCode = LoadFileErrorCode

    def __init__(self):
        self.success = LoadFileErrorCode.no_error
