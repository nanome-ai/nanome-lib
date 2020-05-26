from nanome._internal._structure import _Complex, _Workspace
from nanome._internal._structure._serialization import _ComplexSerializer
from nanome._internal._util._serializers import _ArraySerializer, _TypeSerializer, _StringSerializer

class _ExportFilesItem(_TypeSerializer):
    def __init__(self):
        self.__complex = _ComplexSerializer()
        self.__string = _StringSerializer()

    def version(self):
        return 0

    def name(self):
        return "ExportFilesItem"

    def serialize(self, version, value, context):
        if isinstance(value, _Complex):
            context.write_int(1)
            context.write_using_serializer(self.__complex, value)
        elif isinstance(value, int):
            context.write_int(0)
            context.write_int(value)
        else:
            raise TypeError('Trying to serialize an unsupported type for export files')

    def deserialize(self, version, context):
        result_type = context.read_int()
        if result_type == 0:
            return context.read_using_serializer(self.__string)
        elif result_type == 1:
            return context.read_byte_array()

class _ExportFiles(_TypeSerializer):
    def __init__(self):
        self.__array = _ArraySerializer()
        self.__array.set_type(_ExportFilesItem())

    def version(self):
        return 0

    def name(self):
        return "ExportFiles"

    def serialize(self, version, value, context):
        context.write_int(int(value[0]))
        if (value[1] != None):
            context.write_bool(True)
            context.write_using_serializer(self.__array, value[1])
        else:
            context.write_bool(False)

    def deserialize(self, version, context):
        return context.read_using_serializer(self.__array)