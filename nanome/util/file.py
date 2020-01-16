from . import IntEnum
from .enums import LoadFileErrorCode

class DirectoryErrorCode(IntEnum):
    no_error = 0
    folder_unreachable = 1

class FileErrorCode(IntEnum):
    no_error = 0
    file_unreachable = 1
    path_too_long = 2
    missing_permission = 3

class DirectoryEntry(object):
    def __init__(self):
        self.name = ""
        self.is_directory = False

class FileData(object):
    def __init__(self):
        self.data = None
        self.error_code = FileErrorCode.no_error

class FileSaveData(object):
    def __init__(self):
        self.path = ""
        self.data = bytearray()
        self.error_code = FileErrorCode.no_error

    def write_text(self, text):
        self.data.extend(text.encode('ascii'))

class DirectoryRequestResult(object):
    def __init__(self):
        self.entry_array = []
        self.error_code = DirectoryErrorCode.no_error

class DirectoryRequestOptions(object):
    def __init__(self):
        self._directory_name = "."
        self._pattern = "*"

class LoadInfoDone():
    ErrorCode = LoadFileErrorCode

    def __init__(self):
        self.success = LoadFileErrorCode.no_error
