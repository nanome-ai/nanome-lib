from nanome._internal._util._serializers import _TypeSerializer, _TupleSerializer, _IntSerializer, _StringSerializer

class _TextInputCallback(_TypeSerializer):
    def __init__(self):
        self.__tuple = _TupleSerializer(_IntSerializer(), _StringSerializer())

    def version(self):
        return 0

    def name(self):
        return "TextInputCallback"
        
    def serialize(self, version, value, context):
        context.write_using_serializer(self.__tuple, value)

    def deserialize(self, version, context):
        return context.read_using_serializer(self.__tuple)