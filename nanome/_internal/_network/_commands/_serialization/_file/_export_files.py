from nanome._internal._structure import _Complex, _Workspace
from nanome._internal._structure._serialization import _ComplexSerializer, _AtomSerializer
from nanome._internal._util._serializers import _ArraySerializer, _TypeSerializer, _StringSerializer, _LongSerializer, _DictionarySerializer

class _ExportFilesItem(_TypeSerializer):
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
            context.write_using_serializer(self.__dict, subcontext.payload["Atom"])
            context.write_bytes(subcontext.to_array())
        elif isinstance(value, int):
            context.write_byte(0)
            context.write_long(value)
        else:
            raise TypeError('Trying to serialize an unsupported type for export files')

    def deserialize(self, version, context):
        result_type = context.read_byte()
        if result_type == 0:
            return context.read_using_serializer(self.__string)
        elif result_type == 1:
            res = context.read_byte_array()
            if len(res) == 0:
                return None
            return res

class _ExportFiles(_TypeSerializer):
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