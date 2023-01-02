from nanome._internal.util.serializers import _StringSerializer
from nanome.util.file import FileMeta
from nanome._internal.structure import _Complex, _Workspace
from nanome._internal.util.serializers import TypeSerializer, _StringSerializer, _ArraySerializer
from nanome._internal.util.serializers import _StringSerializer, _ArraySerializer, _FileSaveDataSerializer
from nanome._internal.util.serializers import _StringSerializer, _ArraySerializer, _FileDataSerializer
from nanome.util import DirectoryRequestResult, DirectoryErrorCode
from nanome._internal.util.serializers import _StringSerializer, _ArraySerializer, _DirectoryEntrySerializer
from nanome._internal.util.serializers import TypeSerializer
from nanome._internal.util.serializers import _ArraySerializer, TypeSerializer, _StringSerializer, _LongSerializer, _DictionarySerializer
from nanome._internal.structure.serialization import _ComplexSerializer, _AtomSerializer
from nanome._internal.util.serializers import _StringSerializer, TypeSerializer
from nanome.util import FileError


class _CD(TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "cd"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        return FileError.safe_cast(context.read_int())


class _CP(TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "cp"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value[0])
        context.write_using_serializer(self.__string, value[1])

    def deserialize(self, version, context):
        return FileError.safe_cast(context.read_int())


class _ExportFilesItem(TypeSerializer):
    def __init__(self):
        self.__complex = _ComplexSerializer()
        self.__string = _StringSerializer()
        self.__dict = _DictionarySerializer()
        self.__dict.set_types(_LongSerializer(), _AtomSerializer())

    def version(self):
        return 0

    def name(self):
        return "ExportFilesItem"

    def serialize(self, version, value, context):
        if isinstance(value, _Complex):
            context.write_byte(1)
            subcontext = context.create_sub_context()
            subcontext.payload["Atom"] = {}
            subcontext.write_using_serializer(self.__complex, value)
            context.write_using_serializer(
                self.__dict, subcontext.payload["Atom"])
            context.write_bytes(subcontext.to_array())
        elif isinstance(value, int):
            context.write_byte(0)
            context.write_long(value)
        else:
            raise TypeError(
                'Trying to serialize an unsupported type for export files')

    def deserialize(self, version, context):
        result_type = context.read_byte()
        if result_type == 0:
            return context.read_using_serializer(self.__string)
        elif result_type == 1:
            res = context.read_byte_array()
            if len(res) == 0:
                return None
            return res


class _ExportFiles(TypeSerializer):
    def __init__(self):
        self.__array = _ArraySerializer()
        self.__array.set_type(_ExportFilesItem())

    def version(self):
        return 0

    def name(self):
        return "ExportFiles"

    def serialize(self, version, value, context):
        context.write_byte(int(value[0]))
        if (value[1] != None):
            context.write_bool(True)
            context.write_using_serializer(self.__array, value[1])
        else:
            context.write_bool(False)

    def deserialize(self, version, context):
        return context.read_using_serializer(self.__array)


class _FileMeta(TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "FileMeta"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value.name)
        context.write_long(value.size)
        context.write_using_serializer(self.__string, value.date_modified)
        context.write_bool(value.is_directory)

    def deserialize(self, version, context):
        result = FileMeta()
        result.name = context.read_using_serializer(self.__string)
        result.size = context.read_long()
        result.date_modified = context.read_using_serializer(self.__string)
        result.is_directory = context.read_bool()
        return result


class _Get(TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "get"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        error_code = FileError(context.read_int())
        length = context.read_uint()
        file = context.read_bytes(length)
        return (error_code, file)


class _LS(TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()
        self.__array = _ArraySerializer()
        self.__array.set_type(_FileMeta())

    def version(self):
        return 0

    def name(self):
        return "ls"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        error_code = FileError.safe_cast(context.read_int())
        filemetas = context.read_using_serializer(self.__array)
        return error_code, filemetas


class _MKDir(TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "mkdir"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        return FileError.safe_cast(context.read_int())


class _MV(TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "mv"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value[0])
        context.write_using_serializer(self.__string, value[1])

    def deserialize(self, version, context):
        return FileError.safe_cast(context.read_int())


class _Put(TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "put"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value[0])
        context.write_uint(len(value[1]))
        context.write_bytes(value[1])

    def deserialize(self, version, context):
        return FileError.safe_cast(context.read_int())


class _PWD(TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "pwd"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        error_code = FileError.safe_cast(context.read_int())
        path = context.read_using_serializer(self.__string)
        return (error_code, path)


class _RM(TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "rm"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        return FileError.safe_cast(context.read_int())


class _RMDir(TypeSerializer):
    def __init__(self):
        self.__string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "rmdir"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        return FileError.safe_cast(context.read_int())


class _DirectoryRequest(TypeSerializer):
    # Deprecated
    def __init__(self):
        self.__string = _StringSerializer()
        self.__directory_entry_array = _ArraySerializer()
        self.__directory_entry_array.set_type(_DirectoryEntrySerializer())

    def version(self):
        return 0

    def name(self):
        return "Directory"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value._directory_name)
        context.write_using_serializer(self.__string, value._pattern)

    def deserialize(self, version, context):
        result = DirectoryRequestResult()
        result.entry_array = context.read_using_serializer(
            self.__directory_entry_array)
        result.error_code = DirectoryErrorCode(context.read_int())
        return result


class _FileRequest(TypeSerializer):
    # Deprecated
    def __init__(self):
        self.__string_array = _ArraySerializer()
        self.__string_array.set_type(_StringSerializer())
        self.__file_data_array = _ArraySerializer()
        self.__file_data_array.set_type(_FileDataSerializer())

    def version(self):
        return 0

    def name(self):
        return "FileRequest"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string_array, value)

    def deserialize(self, version, context):
        return context.read_using_serializer(self.__file_data_array)


class _FileSave(TypeSerializer):
    # Deprecated
    def __init__(self):
        self.__file_data_array = _ArraySerializer()
        self.__file_data_array.set_type(_FileSaveDataSerializer())

    def version(self):
        return 0

    def name(self):
        return "FileSave"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__file_data_array, value)

    def deserialize(self, version, context):
        return context.read_using_serializer(self.__file_data_array)
