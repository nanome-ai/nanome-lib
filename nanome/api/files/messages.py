from nanome._internal import serializer_fields
from nanome.util import FileError
from nanome.api import structure


class CD(serializer_fields.TypeSerializer):

    def __init__(self):
        self.__string = serializer_fields.StringField()

    def version(self):
        return 0

    def name(self):
        return "cd"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        return FileError.safe_cast(context.read_int())


class CP(serializer_fields.TypeSerializer):

    def __init__(self):
        self.__string = serializer_fields.StringField()

    def version(self):
        return 0

    def name(self):
        return "cp"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value[0])
        context.write_using_serializer(self.__string, value[1])

    def deserialize(self, version, context):
        from nanome.util import FileError
        return FileError.safe_cast(context.read_int())


class ExportFilesItem(serializer_fields.TypeSerializer):

    def __init__(self):
        self.__complex = structure.serializers.ComplexSerializer()
        self.__string = serializer_fields.StringField()
        self.__dict = serializer_fields.DictionaryField()
        self.__dict.set_types(serializer_fields.LongField(), structure.serializers.AtomSerializer())

    def version(self):
        return 0

    def name(self):
        return "ExportFilesItem"

    def serialize(self, version, value, context):
        if isinstance(value, structure.models._Complex):
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


class ExportFiles(serializer_fields.TypeSerializer):

    def __init__(self):
        self.__array = serializer_fields.ArrayField()
        self.__array.set_type(ExportFilesItem())

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


class FileMeta(serializer_fields.TypeSerializer):

    def __init__(self):
        self.__string = serializer_fields.StringField()

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


class Get(serializer_fields.TypeSerializer):

    def __init__(self):
        self.__string = serializer_fields.StringField()

    def version(self):
        return 0

    def name(self):
        return "get"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        from nanome.util import FileError
        error_code = FileError(context.read_int())
        length = context.read_uint()
        file = context.read_bytes(length)
        return (error_code, file)


class LS(serializer_fields.TypeSerializer):

    def __init__(self):
        self.__string = serializer_fields.StringField()
        self.__array = serializer_fields.ArrayField()
        self.__array.set_type(FileMeta())

    def version(self):
        return 0

    def name(self):
        return "ls"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        from nanome.util import FileError
        error_code = FileError.safe_cast(context.read_int())
        filemetas = context.read_using_serializer(self.__array)
        return error_code, filemetas


class MKDir(serializer_fields.TypeSerializer):

    def __init__(self):
        self.__string = serializer_fields.StringField()

    def version(self):
        return 0

    def name(self):
        return "mkdir"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        from nanome.util import FileError
        return FileError.safe_cast(context.read_int())


class MV(serializer_fields.TypeSerializer):

    def __init__(self):
        self.__string = serializer_fields.StringField()

    def version(self):
        return 0

    def name(self):
        return "mv"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value[0])
        context.write_using_serializer(self.__string, value[1])

    def deserialize(self, version, context):
        from nanome.util import FileError
        return FileError.safe_cast(context.read_int())


class Put(serializer_fields.TypeSerializer):

    def __init__(self):
        self.__string = serializer_fields.StringField()

    def version(self):
        return 0

    def name(self):
        return "put"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value[0])
        context.write_uint(len(value[1]))
        context.write_bytes(value[1])

    def deserialize(self, version, context):
        from nanome.util import FileError
        return FileError.safe_cast(context.read_int())


class PWD(serializer_fields.TypeSerializer):

    def __init__(self):
        self.__string = serializer_fields.StringField()

    def version(self):
        return 0

    def name(self):
        return "pwd"

    def serialize(self, version, value, context):
        pass

    def deserialize(self, version, context):
        from nanome.util import FileError
        error_code = FileError.safe_cast(context.read_int())
        path = context.read_using_serializer(self.__string)
        return (error_code, path)


class RM(serializer_fields.TypeSerializer):

    def __init__(self):
        self.__string = serializer_fields.StringField()

    def version(self):
        return 0

    def name(self):
        return "rm"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        from nanome.util import FileError
        return FileError.safe_cast(context.read_int())


class RMDir(serializer_fields.TypeSerializer):

    def __init__(self):
        self.__string = serializer_fields.StringField()

    def version(self):
        return 0

    def name(self):
        return "rmdir"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value)

    def deserialize(self, version, context):
        from nanome.util import FileError
        return FileError.safe_cast(context.read_int())


class DirectoryRequest(serializer_fields.TypeSerializer):
    # Deprecated
    def __init__(self):
        self.__string = serializer_fields.StringField()
        self.__directory_entry_array = serializer_fields.ArrayField()
        self.__directory_entry_array.set_type(serializer_fields.DirectoryEntryField())

    def version(self):
        return 0

    def name(self):
        return "Directory"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string, value._directory_name)
        context.write_using_serializer(self.__string, value._pattern)

    def deserialize(self, version, context):
        from nanome.util import DirectoryRequestResult, DirectoryErrorCode
        result = DirectoryRequestResult()
        result.entry_array = context.read_using_serializer(
            self.__directory_entry_array)
        result.error_code = DirectoryErrorCode(context.read_int())
        return result


class FileRequest(serializer_fields.TypeSerializer):
    # Deprecated
    def __init__(self):
        self.__string_array = serializer_fields.ArrayField()
        self.__string_array.set_type(serializer_fields.StringField())
        self.__file_data_array = serializer_fields.ArrayField()
        self.__file_data_array.set_type(serializer_fields.FileDataField())

    def version(self):
        return 0

    def name(self):
        return "FileRequest"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__string_array, value)

    def deserialize(self, version, context):
        return context.read_using_serializer(self.__file_data_array)


class FileSave(serializer_fields.TypeSerializer):
    # Deprecated
    def __init__(self):
        self.__file_data_array = serializer_fields.ArrayField()
        self.__file_data_array.set_type(serializer_fields.FileSaveDataField())

    def version(self):
        return 0

    def name(self):
        return "FileSave"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.__file_data_array, value)

    def deserialize(self, version, context):
        return context.read_using_serializer(self.__file_data_array)


class LoadFileInfo(serializer_fields.TypeSerializer):

    def __init__(self):
        self.string = serializer_fields.StringField()

    def version(self):
        return 0

    def name(self):
        return "LoadFileInfo"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.string, value[0])
        context.write_byte_array(value[1])

    def deserialize(self, version, context):
        raise NotImplementedError


class LoadFile(serializer_fields.TypeSerializer):

    def __init__(self):
        self.array = serializer_fields.ArrayField()
        self.array.set_type(LoadFileInfo())

    def version(self):
        return 0

    def name(self):
        return "LoadFile"

    def serialize(self, version, value, context):
        context.write_using_serializer(self.array, value[0])
        context.write_bool(value[1])
        context.write_bool(value[2])

    def deserialize(self, version, context):
        raise NotImplementedError


class LoadFileDoneInfo(serializer_fields.TypeSerializer):

    def version(self):
        return 0

    def name(self):
        return "LoadFileDoneInfo"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        from nanome.util.file import LoadInfoDone
        from nanome.util.enums import LoadFileErrorCode
        result = LoadInfoDone()
        result.success = LoadFileErrorCode(context.read_byte())
        return result


class LoadFileDone(serializer_fields.TypeSerializer):

    def __init__(self):
        self.array = serializer_fields.ArrayField()
        self.array.set_type(LoadFileDoneInfo())

    def version(self):
        return 0

    def name(self):
        return "LoadFileDone"

    def serialize(self, version, value, context):
        raise NotImplementedError

    def deserialize(self, version, context):
        return context.read_using_serializer(self.array)

# classes
